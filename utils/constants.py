# utils/constants.py

SKIN_CLASSES = {
    0: "Eczema",
    1: "Warts",
    2: "Melanoma",
    3: "Atopic Dermatitis",
    4: "Basal Cell Carcinoma",
    5: "Melanocytic Nevi",
    6: "Benign Keratosis-like Lesions",
    7: "Psoriasis",
    8: "Seborrheic Keratoses",
    9: "Fungal Infections"
}

PRODUCT_RECOMMENDATIONS = {
    "Eczema": ["CeraVe Healing Ointment", "Aveeno Eczema Therapy"],
    "Warts": ["Salicylic acid patches", "Cryotherapy"],
    "Melanoma": ["Urgent medical attention needed"],
    "Atopic Dermatitis": ["Moisturizing cream", "Oatmeal Bath"],
    "Basal Cell Carcinoma": ["Consult dermatologist immediately"],
    "Melanocytic Nevi": ["Monitor changes", "SPF 50+"],
    "Benign Keratosis-like Lesions": ["Gentle cleanser", "Hydrating cream"],
    "Psoriasis": ["Corticosteroid Cream", "Coal Tar Shampoo"],
    "Seborrheic Keratoses": ["Non-comedogenic skincare", "Topical treatments"],
    "Fungal Infections": ["Antifungal cream", "Keep area dry"]
}

MODEL_NAME = "davidfred/vit_skin_disease_model"

FACE_DETECTION_MODEL = "facebook/detr-resnet-50"

APP_TITLE = ".Face Detector & Skin Analyzer <3"
WINDOW_SIZE = "800x600"