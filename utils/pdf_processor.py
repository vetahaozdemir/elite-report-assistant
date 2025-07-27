"""
PDF işleme ve metin çıkarma modülü
"""

import os
from typing import List, Dict
import pypdf
from pathlib import Path

class PDFProcessor:
    """PDF dosyalarını işlemek için yardımcı sınıf"""
    
    def __init__(self):
        self.supported_extensions = ['.pdf']
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        PDF dosyasından metin çıkarır
        
        Args:
            pdf_path (str): PDF dosyasının yolu
            
        Returns:
            str: Çıkarılan metin
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                    
            return text.strip()
        except Exception as e:
            print(f"PDF işleme hatası: {e}")
            return ""
    
    def split_text_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Metni anlalmlı parçalara böler
        
        Args:
            text (str): Bölünecek metin
            chunk_size (int): Her parçanın boyutu
            overlap (int): Parçalar arası örtüşme
            
        Returns:
            List[str]: Metin parçaları listesi
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Chunk'ın sonunu bul
            end = start + chunk_size
            
            # Eğer son değilse, cümle sonunu bul
            if end < len(text):
                # Son nokta veya yeni satırı bul
                last_period = text.rfind('.', start, end)
                last_newline = text.rfind('\n', start, end)
                
                # En yakın uygun noktayı seç
                if last_period > start:
                    end = last_period + 1
                elif last_newline > start:
                    end = last_newline + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Sonraki başlangıç noktası (örtüşme ile)
            start = max(start + chunk_size - overlap, end)
        
        return chunks
    
    def process_pdf_file(self, pdf_path: str, chunk_size: int = 1000, overlap: int = 200) -> Dict:
        """
        PDF dosyasını işler ve metadata ile birlikte döndürür
        
        Args:
            pdf_path (str): PDF dosyasının yolu
            chunk_size (int): Chunk boyutu
            overlap (int): Örtüşme miktarı
            
        Returns:
            Dict: İşlenmiş veri (chunks, metadata)
        """
        file_path = Path(pdf_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {pdf_path}")
        
        if file_path.suffix.lower() not in self.supported_extensions:
            raise ValueError(f"Desteklenmeyen dosya formatı: {file_path.suffix}")
        
        # Metin çıkar
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text:
            raise ValueError("PDF'den metin çıkarılamadı")
        
        # Metni parçalara böl
        chunks = self.split_text_into_chunks(text, chunk_size, overlap)
        
        # Metadata oluştur
        metadata = {
            'filename': file_path.name,
            'file_path': str(file_path),
            'file_size': file_path.stat().st_size,
            'total_chunks': len(chunks),
            'total_characters': len(text)
        }
        
        return {
            'chunks': chunks,
            'metadata': metadata,
            'full_text': text
        }
    
    def process_directory(self, directory_path: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict]:
        """
        Bir klasördeki tüm PDF dosyalarını işler
        
        Args:
            directory_path (str): Klasör yolu
            chunk_size (int): Chunk boyutu
            overlap (int): Örtüşme miktarı
            
        Returns:
            List[Dict]: İşlenmiş dosyalar listesi
        """
        directory = Path(directory_path)
        
        if not directory.exists():
            raise FileNotFoundError(f"Klasör bulunamadı: {directory_path}")
        
        processed_files = []
        
        for file_path in directory.glob("*.pdf"):
            try:
                result = self.process_pdf_file(str(file_path), chunk_size, overlap)
                processed_files.append(result)
                print(f"İşlendi: {file_path.name}")
            except Exception as e:
                print(f"Hata ({file_path.name}): {e}")
        
        return processed_files