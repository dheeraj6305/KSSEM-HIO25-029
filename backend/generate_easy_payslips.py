# generate_easy_payslips.py
from PIL import Image, ImageDraw
import random, os

# Output folder
OUT_DIR = "sample_data/salary_slip_samples"
os.makedirs(OUT_DIR, exist_ok=True)

# Number of payslips to generate
N = 200   # You can change to 500 or 1000 later

for i in range(1, N + 1):
    # Generate random salary between 20k and 1 lakh
    salary = random.randint(20000, 100000)
    name = f"Employee_{i}"

    # Create a white image
    img = Image.new("RGB", (800, 400), color="white")
    draw = ImageDraw.Draw(img)

    # Write clean text (OCR-friendly)
    draw.text((50, 80), f"Company: Nexus Bank", fill="black")
    draw.text((50, 130), f"Employee Name: {name}", fill="black")
    draw.text((50, 180), f"Salary: {salary}", fill="black")

    # Save as JPG
    img.save(os.path.join(OUT_DIR, f"{name}.jpg"), quality=90)

print(f"✅ Generated {N} clean sample payslips in {OUT_DIR}")
