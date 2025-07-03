import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

late List<CameraDescription> cameras;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();
  runApp(const MyApp());
}

class FaceBox {
  final String name;
  final Rect rect;
  FaceBox({required this.name, required this.rect});
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: CameraApp(),
    );
  }
}

class CameraApp extends StatefulWidget {
  const CameraApp({super.key});
  @override
  _CameraAppState createState() => _CameraAppState();
}

class _CameraAppState extends State<CameraApp> {
  CameraController? _controller;
  int _cameraIndex = 0;
  final List<FaceBox> _boxes = [];
  bool _sending = false;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _initCamera(_cameraIndex);
  }

  Future<void> _initCamera(int index) async {
    await _controller?.dispose();
    final desc = cameras[index];
    _controller = CameraController(
      desc,
      ResolutionPreset.medium,
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.jpeg,
    );
    await _controller!.initialize();
    if (mounted) setState(() {});
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(milliseconds: 700), (_) {
      if (!_sending) _sendFrame();
    });
  }

  Future<void> _sendFrame() async {
    if (!(_controller?.value.isInitialized ?? false)) return;
    _sending = true;
    try {
      final image = await _controller!.takePicture();
      final bytes = await image.readAsBytes();

      final uri = Uri.parse('http://192.168.18.21:8000/api/recognize');
      final request = http.MultipartRequest('POST', uri)
        ..files.add(
          http.MultipartFile.fromBytes(
            'file',
            bytes,
            filename: 'frame.jpg',
            contentType: MediaType('image', 'jpeg'),
          ),
        );

      final response = await request.send().timeout(const Duration(seconds: 5));
      final body = await response.stream.bytesToString();
      final data = jsonDecode(body) as List<dynamic>;

      if (mounted) {
        setState(() {
          _boxes.clear();
          for (var item in data) {
            final bbox = item['bbox'] as List;
            final rect = Rect.fromLTWH(
              bbox[0].toDouble(),
              bbox[1].toDouble(),
              (bbox[2] - bbox[0]).toDouble(),
              (bbox[3] - bbox[1]).toDouble(),
            );
            _boxes.add(FaceBox(name: item['name'], rect: rect));
          }
        });
      }
    } catch (e) {
      debugPrint('Error enviando frame: $e');
    } finally {
      _sending = false;
    }
  }

  Future<void> _switchCamera() async {
    _timer?.cancel();
    if (_controller != null) {
      await _controller!.dispose();
      _controller = null;
    }
    setState(() {
      _boxes.clear();
      _sending = false;
    });
    _cameraIndex = (_cameraIndex + 1) % cameras.length;
    await _initCamera(_cameraIndex);
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final previewSize = _controller!.value.previewSize!;
    final screenSize = MediaQuery.of(context).size;
    final isFrontCamera = cameras[_cameraIndex].lensDirection == CameraLensDirection.front;

    return Scaffold(
      body: Stack(
        children: [
          Center(
            child: AspectRatio(
              aspectRatio: previewSize.height / previewSize.width, // width/height invertido usualmente
              child: CameraPreview(_controller!),
            ),
          ),
          Positioned.fill(
            child: IgnorePointer(
              child: CustomPaint(
                painter: FaceBoxPainter(
                  _boxes,
                  Size(previewSize.height, previewSize.width),
                  screenSize,
                  fit: BoxFit.contain,
                  isFrontCamera: isFrontCamera,
                ),
              ),
            ),
          ),
          Positioned(
            top: 50,
            right: 20,
            child: FloatingActionButton(
              onPressed: _switchCamera,
              child: const Icon(Icons.cameraswitch),
            ),
          ),
        ],
      ),
    );
  }
}

class FaceBoxPainter extends CustomPainter {
  final List<FaceBox> boxes;
  final Size imageSize;
  final Size previewSize;
  final BoxFit fit;
  final bool isFrontCamera;

  FaceBoxPainter(
    this.boxes,
    this.imageSize,
    this.previewSize, {
    this.fit = BoxFit.contain,
    this.isFrontCamera = false,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.green
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    final outputRect = _applyBoxFit(fit, imageSize, previewSize);
    final scaleX = outputRect.width / imageSize.width;
    final scaleY = outputRect.height / imageSize.height;
    final offsetX = outputRect.left;
    final offsetY = outputRect.top;

    for (var box in boxes) {
      double left = box.rect.left;
      double width = box.rect.width;

      // Espejado horizontal para cámara frontal
      if (isFrontCamera) {
        left = imageSize.width - (box.rect.left + box.rect.width);
      }

      final rect = Rect.fromLTRB(
        left * scaleX + offsetX,
        box.rect.top * scaleY + offsetY,
        (left + width) * scaleX + offsetX,
        (box.rect.top + box.rect.height) * scaleY + offsetY,
      );
      canvas.drawRect(rect, paint);

      // Etiqueta
      final textSpan = TextSpan(
        text: box.name,
        style: const TextStyle(color: Colors.white, fontSize: 14, backgroundColor: Colors.green),
      );
      final textPainter = TextPainter(text: textSpan, textDirection: TextDirection.ltr)..layout();
      textPainter.paint(canvas, Offset(rect.left, rect.top - textPainter.height));
    }
  }

  @override
  bool shouldRepaint(FaceBoxPainter oldDelegate) => true;

  Rect _applyBoxFit(BoxFit fit, Size input, Size output) {
    final inputAR = input.width / input.height;
    final outputAR = output.width / output.height;
    if ((fit == BoxFit.contain && inputAR > outputAR) ||
        (fit == BoxFit.cover && inputAR < outputAR)) {
      final scale = output.width / input.width;
      final height = input.height * scale;
      final top = (output.height - height) / 2;
      return Rect.fromLTWH(0, top, output.width, height);
    } else {
      final scale = output.height / input.height;
      final width = input.width * scale;
      final left = (output.width - width) / 2;
      return Rect.fromLTWH(left, 0, width, output.height);
    }
  }
}
