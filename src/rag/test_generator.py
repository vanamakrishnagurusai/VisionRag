from src.rag.generator import RAGGenerator


def main():

    generator = RAGGenerator()

    results = [
        {
            "filename": "image_001.jpg",
            "score": 0.82,
            "caption": (
                "a person standing next to a car"
            ),
            "objects": [
                {
                    "class": "person",
                    "confidence": 0.91
                },
                {
                    "class": "car",
                    "confidence": 0.87
                }
            ],
            "multimodal_context": (
                "Image caption: a person standing "
                "next to a car. Detected objects: "
                "one person, one car. "
                "Object positions: person at "
                "center-left, car at center-right."
            )
        }
    ]

    answer = generator.generate_answer(
        "Is there a person near a car?",
        results
    )

    print("\nVisionRAG Answer:")
    print(answer)


if __name__ == "__main__":
    main()