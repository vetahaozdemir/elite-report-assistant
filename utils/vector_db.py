"""
ChromaDB vektör veritabanı modülü
"""

import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from typing import List, Dict, Optional
import os
from pathlib import Path

class VectorDatabase:
    """ChromaDB ile vektör veritabanı yönetimi"""
    
    def __init__(self, db_path: str = "./data/vector_db", api_key: str = None):
        """
        VectorDatabase initialization
        
        Args:
            db_path (str): Veritabanı dosya yolu
            api_key (str): Gemini API anahtarı
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # ChromaDB client oluştur
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Gemini API yapılandır
        if api_key:
            genai.configure(api_key=api_key)
        elif os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        else:
            print("Uyarı: GEMINI_API_KEY çevre değişkeni bulunamadı")
        
        # Embedding model
        self.embedding_model = "models/text-embedding-004"
        
        # Collection oluştur veya al
        self.collection_name = "sosyal_raporlar"
        self.collection = self.get_or_create_collection()
    
    def get_or_create_collection(self):
        """Collection oluştur veya mevcut olanı al"""
        try:
            collection = self.client.get_collection(self.collection_name)
            print(f"Mevcut collection bulundu: {self.collection_name}")
        except:
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Sosyal hizmet raporları vektör veritabanı"}
            )
            print(f"Yeni collection oluşturuldu: {self.collection_name}")
        
        return collection
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Metin için embedding oluştur
        
        Args:
            text (str): Embedding oluşturulacak metin
            
        Returns:
            List[float]: Embedding vektörü
        """
        try:
            response = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return response['embedding']
        except Exception as e:
            print(f"Embedding oluşturma hatası: {e}")
            return []
    
    def add_document(self, document_id: str, text: str, metadata: Dict = None) -> bool:
        """
        Veritabanına dokuman ekle
        
        Args:
            document_id (str): Benzersiz dokuman ID
            text (str): Dokuman metni
            metadata (Dict): Ek metadata bilgileri
            
        Returns:
            bool: İşlem başarılı mı
        """
        try:
            # Embedding oluştur
            embedding = self.generate_embedding(text)
            
            if not embedding:
                print("Embedding oluşturulamadı")
                return False
            
            # Metadata hazırla
            doc_metadata = metadata or {}
            doc_metadata.update({
                'character_count': len(text),
                'word_count': len(text.split())
            })
            
            # Veritabanına ekle
            self.collection.add(
                ids=[document_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[doc_metadata]
            )
            
            return True
            
        except Exception as e:
            print(f"Dokuman ekleme hatası: {e}")
            return False
    
    def add_multiple_documents(self, documents: List[Dict]) -> int:
        """
        Birden fazla dokuman ekle
        
        Args:
            documents (List[Dict]): Dokuman listesi (id, text, metadata içeren dict'ler)
            
        Returns:
            int: Başarıyla eklenen dokuman sayısı
        """
        added_count = 0
        
        for doc in documents:
            doc_id = doc.get('id')
            text = doc.get('text')
            metadata = doc.get('metadata', {})
            
            if doc_id and text:
                if self.add_document(doc_id, text, metadata):
                    added_count += 1
                    print(f"Eklendi: {doc_id}")
                else:
                    print(f"Eklenemedi: {doc_id}")
        
        return added_count
    
    def search_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Benzer dokümanları ara
        
        Args:
            query (str): Arama sorgusu
            n_results (int): Döndürülecek sonuç sayısı
            
        Returns:
            List[Dict]: Benzer dokümanlar
        """
        try:
            # Query için embedding oluştur
            query_embedding = self.generate_embedding(query)
            
            if not query_embedding:
                print("Query embedding oluşturulamadı")
                return []
            
            # Arama yap
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Sonuçları formatla
            formatted_results = []
            
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][i] if results['ids'] else None,
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"Arama hatası: {e}")
            return []
    
    def get_collection_stats(self) -> Dict:
        """Collection istatistiklerini al"""
        try:
            count = self.collection.count()
            return {
                'document_count': count,
                'collection_name': self.collection_name,
                'db_path': str(self.db_path)
            }
        except Exception as e:
            print(f"İstatistik hatası: {e}")
            return {}
    
    def delete_document(self, document_id: str) -> bool:
        """Dokuman sil"""
        try:
            self.collection.delete(ids=[document_id])
            return True
        except Exception as e:
            print(f"Silme hatası: {e}")
            return False
    
    def clear_collection(self) -> bool:
        """Collection'ı temizle"""
        try:
            # Collection'ı sil ve yeniden oluştur
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Sosyal hizmet raporları vektör veritabanı"}
            )
            return True
        except Exception as e:
            print(f"Temizleme hatası: {e}")
            return False