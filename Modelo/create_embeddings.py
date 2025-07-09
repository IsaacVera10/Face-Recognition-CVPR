import os
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
from tqdm import tqdm
import torch
import faiss
from facenet_pytorch import MTCNN, InceptionResnetV1

# === CONFIGURACIÓN GENERAL ===
DATASET_PATH = 'known_faces'
USE_AUGMENTATION = True  # Cambia a False si no quieres usarlo
EMBEDDING_DIM = 512
RESIZE_TO = 160

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# === Manejo de compatibilidad con Pillow ===
try:
    RESAMPLE = Image.Resampling.LANCZOS  # Pillow >= 10
except AttributeError:
    RESAMPLE = Image.ANTIALIAS  # Pillow < 10

# === MODELOS ===
mtcnn = MTCNN(image_size=RESIZE_TO, margin=10, device=device)
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

embedding_list = []
name_list = []
user_id_list = []

# === FUNCIONES DE AUMENTO ===
def augment_image(image):
    augmented = []

    # 1. Flip horizontal
    augmented.append(ImageOps.mirror(image))

    # 2. Jitter de brillo y contraste
    for factor in [0.7, 1.3]:
        bright = ImageEnhance.Brightness(image).enhance(factor)
        contrast = ImageEnhance.Contrast(bright).enhance(factor)
        augmented.append(contrast)

    # 3. Gaussian blur
    blurred = image.filter(ImageFilter.GaussianBlur(radius=1.5))
    augmented.append(blurred)

    # 4. Rotación leve
    for angle in [-8, 8]:
        rotated = image.rotate(angle)
        augmented.append(rotated)

    return augmented


folder_to_user_id = {
    "aaron_camacho": "ID-99887766",
    "alejandro_calizaya": "ID-92448566",
    "alexander_guzman": "ID-14548807",
    "alexandro_chamochumbi": "ID-70863919",
    "anderson_carcamo": "ID-44670683",
    "andres_riveros": "ID-65963712",
    "bladimir_alferez": "ID-59635194",
    "davi_magalhaes": "ID-83702853",
    "dimael_rivas": "ID-44065136",
    "edgar_chambilla": "ID-74137749",
    "enzo_camizan": "ID-61123267",
    "ernesto_ormeno": "ID-10488529",
    "gonzalo_alfaro": "ID-67206004",
    "isaac_vera": "ID-87654321",
    "jose_chachi": "ID-90790501",
    "jose_pinedo": "ID-23638406",
    "jose_wong": "ID-62801755",
    "josue_arriaga": "ID-28474510",
    "juan_leandro": "ID-84146819",
    "kelvin_cahuana": "ID-95271987",
    "luis_gutierrez": "ID-19169349",
    "luis_mendez": "ID-55667788",
    "luis_torres": "ID-11223344",
    "marcos_ayala": "ID-46151114",
    "margiory_alvarado": "ID-61209124",
    "max_antunez": "ID-68732545",
    "nicolas_arroyo": "ID-55890342",
    "rensso_mora": "ID-99759795",
    "stuart_arteaga": "ID-47721320",
}


# === RECORRER TODAS LAS IMÁGENES ===
for person_name in tqdm(os.listdir(DATASET_PATH), desc="Procesando personas"):
    person_dir = os.path.join(DATASET_PATH, person_name)
    if not os.path.isdir(person_dir):
        continue
    
    user_id = folder_to_user_id[person_name] if person_name in folder_to_user_id else "ID-UNKNOWN"

    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)

        try:
            img = Image.open(img_path).convert('RGB')
        except:
            print(f"❌ Error abriendo {img_path}")
            continue

        # Resize si es menor
        if img.size != (RESIZE_TO, RESIZE_TO):
            img = img.resize((RESIZE_TO, RESIZE_TO), RESAMPLE)

        # Detectar rostro
        face = mtcnn(img)
        if face is not None:
            face = face.unsqueeze(0).to(device)
            with torch.no_grad():
                embedding = model(face).cpu().numpy().flatten()
                embedding_list.append(embedding)
                user_id_list.append(user_id)
        else:
            print(f"⚠️ No se detectó rostro en {img_path}")

        # === Aumentos ===
        if USE_AUGMENTATION:
            aug_imgs = augment_image(img)
            for aug in aug_imgs:
                face_aug = mtcnn(aug)
                if face_aug is not None:
                    face_aug = face_aug.unsqueeze(0).to(device)
                    with torch.no_grad():
                        embedding = model(face_aug).cpu().numpy().flatten()
                        embedding_list.append(embedding)
                        user_id_list.append(person_name)

# === GUARDAR .npy ===
embeddings = np.array(embedding_list)
user_ids = np.array(user_id_list)

np.save('embeddings.npy', embeddings)
np.save('user_ids.npy', user_ids)
print(f"✅ Embeddings generados: {embeddings.shape[0]} vectores guardados.")

# === INDEXAR EN FAISS ===
index = faiss.IndexFlatL2(EMBEDDING_DIM)
index.add(embeddings.astype('float32'))
faiss.write_index(index, "faiss_index_uid.bin")
print("✅ Índice FAISS guardado como 'faiss_index_uid.bin'")
