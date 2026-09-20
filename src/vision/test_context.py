from src.vision.context_generator import generate_visual_context


sample_data = {
    "objects": [
        {
            "class": "person",
            "confidence": 0.94,
            "bbox": [100, 100, 300, 500]
        },
        {
            "class": "car",
            "confidence": 0.91,
            "bbox": [400, 200, 900, 600]
        },
        {
            "class": "car",
            "confidence": 0.87,
            "bbox": [950, 200, 1400, 600]
        }
    ]
}


context = generate_visual_context(
    sample_data
)

print(context)