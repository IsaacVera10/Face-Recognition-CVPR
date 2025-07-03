import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
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
  final desc = cameras[index];
  final newController = CameraController(
    desc,
    ResolutionPreset.medium,
    enableAudio: false,
    imageFormatGroup: ImageFormatGroup.jpeg,
  );
  await newController.initialize();
  if (!mounted) return;
  setState(() {
    _controller = newController;
  });
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
            // INTERCAMBIO X/Y para ajustar rotación 90° entre imagen y preview
            final rect = Rect.fromLTWH(
              bbox[1].toDouble(), // x <-- y1
              bbox[0].toDouble(), // y <-- x1
              (bbox[3] - bbox[1]).toDouble(), // width  <-- (y2 - y1)
              (bbox[2] - bbox[0]).toDouble(), // height <-- (x2 - x1)
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

    final size = MediaQuery.of(context).size;
    final preview = _controller!.value.previewSize!;

    // Ahora escalamos con los ejes originales (no rotados)
    final scaleX = size.width / preview.width;
    final scaleY = size.height / preview.height;

    return Scaffold(
      body: Stack(
        children: [
          CameraPreview(_controller!),
          ..._boxes.map((box) {
            return Positioned(
              left: box.rect.left * scaleX,
              top: box.rect.top * scaleY,
              width: box.rect.width * scaleX,
              height: box.rect.height * scaleY,
              child: Container(
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.green, width: 2),
                ),
                child: Align(
                  alignment: Alignment.topLeft,
                  child: Container(
                    color: Colors.green,
                    padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
                    child: Text(box.name, style: const TextStyle(color: Colors.white, fontSize: 12)),
                  ),
                ),
              ),
            );
          }),
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
