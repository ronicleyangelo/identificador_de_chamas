from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import os

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        # Abrir o QFileDialog para selecionar a imagem
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Selecione a Imagem", "", "Imagens (*.png *.jpg *.bmp)")
        
        if not self.image_path:  # Se não selecionar uma imagem, sair do programa
            print("Nenhuma imagem selecionada. Saindo.")
            exit()

        self.image = QPixmap(self.image_path)  # Carregar a imagem
        self.setWindowTitle("Captura de Coordenadas")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(self.image.size())  # Tamanho fixo baseado no tamanho da imagem

        # Definir o nome do arquivo de coordenadas com o mesmo nome da imagem, mas na pasta 'labels/train'
        image_name = os.path.basename(self.image_path)
        self.coords_file = os.path.join("C:/Users/ronicley/OneDrive/Documentos/yolov5/data/labels/train", os.path.splitext(image_name)[0] + ".txt")

        # Garantir que a pasta exista
        os.makedirs(os.path.dirname(self.coords_file), exist_ok=True)

        self.class_id = 0  # Definir um ID para a classe (por exemplo, 0 para a classe "fogo")

    def paintEvent(self, event):
        # Esse método é chamado para desenhar a imagem no widget
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image)  # Desenhando a imagem no canto superior esquerdo

    def mousePressEvent(self, event):
        # Captura as coordenadas x, y do clique
        x = event.pos().x()
        y = event.pos().y()
        
        # Normalizar as coordenadas
        x_center = x / self.image.width()
        y_center = y / self.image.height()
        
        # A largura e altura da caixa delimitadora podem ser fixas ou calculadas conforme necessário.
        # Aqui, vamos salvar uma caixa de 10% da largura e 10% da altura da imagem, como exemplo:
        largura = 0.1  # 10% da largura da imagem
        altura = 0.1   # 10% da altura da imagem

        print(f"Coordenadas clicadas: ({x}, {y}) - Normalizadas: ({x_center:.4f}, {y_center:.4f})")  # Exibe as coordenadas no terminal

        # Salvar as coordenadas no arquivo de texto na pasta 'labels/train' no formato esperado pelo YOLOv5
        with open(self.coords_file, "a") as file:
            file.write(f"{self.class_id} {x_center:.4f} {y_center:.4f} {largura:.4f} {altura:.4f}\n")  # Salva as coordenadas normalizadas

if __name__ == "__main__":
    app = QApplication([])  # Criação da aplicação Qt
    window = ImageViewer()  # Criação da janela principal
    window.show()  # Exibe a janela
    app.exec_()  # Executa o loop de eventos da aplicação
