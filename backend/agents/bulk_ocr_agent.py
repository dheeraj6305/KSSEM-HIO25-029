import os, concurrent.futures, time, csv
from agents.ocr_agent import extract_salary_from_image

def bulk_extract_salary(input_folder: str, output_csv: str = "bulk_ocr_results.csv", max_workers: int = 8):
    start = time.time()
    image_files = [os.path.join(input_folder, f)
                   for f in os.listdir(input_folder)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf'))]

    print(f"🔍 Found {len(image_files)} files in {input_folder}")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(extract_salary_from_image, f): f for f in image_files}
        for future in concurrent.futures.as_completed(future_to_file):
            fpath = future_to_file[future]
            try:
                res = future.result()
                res["file"] = os.path.basename(fpath)
                results.append(res)
            except Exception as e:
                print(f"❌ Error in {fpath}: {e}")

    # Save to CSV
    with open(output_csv, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "salary", "confidence", "raw_text"])
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ OCR done for {len(results)} files in {round(time.time()-start, 2)}s → {output_csv}")
    return results
