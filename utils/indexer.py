"""
PDF dosyalarını indeksleme ve vektör veritabanına ekleme modülü
"""

import os
import uuid
from pathlib import Path
from typing import List, Dict
from .pdf_processor import PDFProcessor
from .vector_db import VectorDatabase

class DocumentIndexer:
    """PDF dosyalarını işleyip vektör veritabanına ekleyen sınıf"""
    
    def __init__(self, vector_db: VectorDatabase = None, api_key: str = None):
        """
        DocumentIndexer initialization
        
        Args:
            vector_db (VectorDatabase): Mevcut VectorDatabase instance
            api_key (str): Gemini API key
        """
        self.pdf_processor = PDFProcessor()
        self.vector_db = vector_db or VectorDatabase(api_key=api_key)
    
    def index_single_file(self, file_path: str, chunk_size: int = 1000, overlap: int = 200) -> int:
        """
        Tek bir PDF dosyasını indeksle
        
        Args:
            file_path (str): PDF dosya yolu
            chunk_size (int): Chunk boyutu
            overlap (int): Örtüşme miktarı
            
        Returns:
            int: Eklenen chunk sayısı
        """
        try:
            # PDF'i işle
            processed_data = self.pdf_processor.process_pdf_file(file_path, chunk_size, overlap)
            
            # Her chunk için dokuman oluştur
            documents = []
            base_filename = Path(file_path).stem
            
            for i, chunk in enumerate(processed_data['chunks']):
                doc_id = f"{base_filename}_chunk_{i}_{uuid.uuid4().hex[:8]}"
                
                metadata = {
                    'source_file': processed_data['metadata']['filename'],
                    'file_path': file_path,
                    'chunk_index': i,
                    'total_chunks': processed_data['metadata']['total_chunks'],
                    'file_size': processed_data['metadata']['file_size'],
                    'document_type': 'social_service_report'
                }
                
                documents.append({
                    'id': doc_id,
                    'text': chunk,
                    'metadata': metadata
                })
            
            # Veritabanına ekle
            added_count = self.vector_db.add_multiple_documents(documents)
            
            print(f"✅ {file_path} dosyasından {added_count}/{len(documents)} chunk eklendi")
            return added_count
            
        except Exception as e:
            print(f"❌ {file_path} dosyası indekslenirken hata: {e}")
            return 0
    
    def index_directory(self, directory_path: str, chunk_size: int = 1000, overlap: int = 200) -> Dict:
        """
        Bir klasördeki tüm PDF dosyalarını indeksle
        
        Args:
            directory_path (str): Klasör yolu
            chunk_size (int): Chunk boyutu
            overlap (int): Örtüşme miktarı
            
        Returns:
            Dict: İndeksleme sonuç raporu
        """
        directory = Path(directory_path)
        
        if not directory.exists():
            raise FileNotFoundError(f"Klasör bulunamadı: {directory_path}")
        
        pdf_files = list(directory.glob("*.pdf"))
        
        if not pdf_files:
            print(f"⚠️  {directory_path} klasöründe PDF dosyası bulunamadı")
            return {
                'total_files': 0,
                'processed_files': 0,
                'total_chunks': 0,
                'failed_files': []
            }
        
        total_chunks = 0
        processed_files = 0
        failed_files = []
        
        print(f"📂 {len(pdf_files)} PDF dosyası bulundu")
        print("🔄 İndeksleme başlıyor...")
        
        for file_path in pdf_files:
            try:
                chunks_added = self.index_single_file(str(file_path), chunk_size, overlap)
                if chunks_added > 0:
                    total_chunks += chunks_added
                    processed_files += 1
                else:
                    failed_files.append(str(file_path))
            except Exception as e:
                print(f"❌ {file_path.name}: {e}")
                failed_files.append(str(file_path))
        
        # Sonuç raporu
        result = {
            'total_files': len(pdf_files),
            'processed_files': processed_files,
            'total_chunks': total_chunks,
            'failed_files': failed_files
        }
        
        print("\n📊 İndeksleme Raporu:")
        print(f"   📁 Toplam dosya: {result['total_files']}")
        print(f"   ✅ İşlenen dosya: {result['processed_files']}")
        print(f"   📄 Toplam chunk: {result['total_chunks']}")
        print(f"   ❌ Başarısız: {len(result['failed_files'])}")
        
        if result['failed_files']:
            print("\n⚠️  Başarısız dosyalar:")
            for file in result['failed_files']:
                print(f"   - {Path(file).name}")
        
        return result
    
    def get_database_stats(self) -> Dict:
        """Vektör veritabanı istatistiklerini al"""
        return self.vector_db.get_collection_stats()
    
    def search_documents(self, query: str, n_results: int = 5) -> List[Dict]:
        """Dokümanlarda arama yap"""
        return self.vector_db.search_similar(query, n_results)
    
    def clear_database(self) -> bool:
        """Veritabanını temizle"""
        return self.vector_db.clear_collection()

def main():
    """Standalone indeksleme scripti"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PDF dosyalarını vektör veritabanına indeksle")
    parser.add_argument("--directory", "-d", type=str, help="İndekslenecek klasör")
    parser.add_argument("--file", "-f", type=str, help="İndekslenecek tek dosya")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk boyutu")
    parser.add_argument("--overlap", type=int, default=200, help="Örtüşme miktarı")
    parser.add_argument("--clear", action="store_true", help="Veritabanını temizle")
    parser.add_argument("--stats", action="store_true", help="Veritabanı istatistiklerini göster")
    
    args = parser.parse_args()
    
    # API key kontrolü
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY çevre değişkeni bulunamadı")
        return
    
    indexer = DocumentIndexer(api_key=api_key)
    
    if args.clear:
        print("🗑️  Veritabanı temizleniyor...")
        if indexer.clear_database():
            print("✅ Veritabanı temizlendi")
        else:
            print("❌ Temizleme başarısız")
        return
    
    if args.stats:
        stats = indexer.get_database_stats()
        print("📊 Veritabanı İstatistikleri:")
        print(f"   📄 Dokuman sayısı: {stats.get('document_count', 0)}")
        print(f"   📁 Collection: {stats.get('collection_name', 'N/A')}")
        print(f"   💾 Veritabanı yolu: {stats.get('db_path', 'N/A')}")
        return
    
    if args.file:
        print(f"📄 Tek dosya indeksleniyor: {args.file}")
        chunks_added = indexer.index_single_file(args.file, args.chunk_size, args.overlap)
        print(f"✅ {chunks_added} chunk eklendi")
    
    elif args.directory:
        print(f"📂 Klasör indeksleniyor: {args.directory}")
        result = indexer.index_directory(args.directory, args.chunk_size, args.overlap)
        print("✅ İndeksleme tamamlandı")
    
    else:
        print("❌ --directory veya --file parametresi gerekli")
        parser.print_help()

if __name__ == "__main__":
    main()