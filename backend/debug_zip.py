import zipfile, os, tempfile

# 🧩 Change this path to your actual ZIP file path
zip_path = r"C:\Users\Monika B\Desktop\KSSEM-HIO25-029\backend\sample_data\salary_slip_samples.zip"

# Create a temporary folder to extract into
temp_dir = tempfile.mkdtemp()

print("📦 Extracting ZIP file from:", zip_path)
try:
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(temp_dir)
except Exception as e:
    print("❌ Failed to open ZIP:", e)
    exit()

print("✅ Extracted into:", temp_dir)
print("\n🗂️ Files found inside:")
for root, _, files in os.walk(temp_dir):
    for f in files:
        print("  -", os.path.join(root, f))
