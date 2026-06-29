# Energybae Solar Load Calculator

AI-powered tool to automate electricity bill analysis and solar system sizing.

## What it does
1. Upload MSEDCL electricity bill (JPG/PNG)
2. AI extracts key data — consumer details, monthly units, bill amount
3. Fills Excel template with solar load calculations
4. Download filled Excel — ready to use

## Tech Stack
- Python + Streamlit (UI)
- Claude Vision API / Gemini Vision API (bill reading)
- openpyxl (Excel generation)

## How to run
pip install streamlit openpyxl pillow google-generativeai anthropic
streamlit run app.py

## Files
- app.py — Streamlit UI
- extractor.py — AI bill extraction (Claude + Gemini)
- excel_filler.py — Excel template filling

## What I would improve next
- Auto-fetch bill from MSEDCL portal using consumer number
- Support PDF bills
- Batch processing multiple bills at once
- RAG system to query across all processed bills