from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, Paragraph
import os
from datetime import datetime

conexao = sqlite3.connect('bdFinanceiro.db')
numeroIDcolab = 0
numeroIDgastos = 0
saldo = 0
saida = 0


def gerar_pdf():
    c = canvas.Canvas("financeiroIBF.pdf", pagesize=A4)
    conexao = sqlite3.connect('bdFinanceiro.db')
    cursor = conexao.cursor()
    comandoSQLColab = 'SELECT nome, cargo, segmento, valor FROM colaboradores ORDER BY segmento ASC, valor DESC'
    cursor.execute(comandoSQLColab)
    leituraBancoColab = cursor.fetchall()

    x = 25
    y = 700

    largura_colunas = [200, 150, 150, 50]

    tamanho_fonte_cabecalho = 15
    tamanho_fonte_dados = 14

    cor_fundo1 = colors.white
    cor_fundo2 = colors.lightgrey

    cabecalho_colab = ["NOME", "CARGO", "SEGMENTO", "VALOR"]
    for i in range(len(cabecalho_colab)):
        c.setFont("Helvetica-Bold", tamanho_fonte_cabecalho)
        c.drawString(x + sum(largura_colunas[:i]), y, cabecalho_colab[i])

    for i, dados in enumerate(leituraBancoColab):
        cor_fundo = cor_fundo1 if i % 2 == 0 else cor_fundo2 
        for j in range(len(dados)):
            c.setFont("Helvetica", tamanho_fonte_dados)  
            c.setFillColor(cor_fundo) 
            c.rect(x + sum(largura_colunas[:j]), y - (i + 1) * 20, largura_colunas[j], 20, fill=True)
            c.setFillColor(colors.black)
            c.drawString(x + sum(largura_colunas[:j]) + 5, y - (i + 1) * 20 + 5, str(dados[j]))

    espacamento = 25

    y_gastos = y - (len(leituraBancoColab) + 2) * 20 - espacamento

    comandoSQLGastos = 'SELECT descricao, quantia FROM gastos'
    cursor.execute(comandoSQLGastos)
    leituraBancoGastos = cursor.fetchall()

    largura_colunas_gastos = [500, 50]

    cabecalho_gastos = ["DESCRIÇÃO", "VALOR"]
    for i in range(len(cabecalho_gastos)):
        c.setFont("Helvetica-Bold", tamanho_fonte_cabecalho)
        c.drawString(x + sum(largura_colunas_gastos[:i]), y_gastos, cabecalho_gastos[i])

    for i, dados in enumerate(leituraBancoGastos):
        cor_fundo = cor_fundo1 if i % 2 == 0 else cor_fundo2
        for j in range(len(dados)):
            c.setFont("Helvetica", tamanho_fonte_dados)
            c.setFillColor(cor_fundo)
            c.rect(x + sum(largura_colunas_gastos[:j]), y_gastos - (i + 1) * 20, largura_colunas_gastos[j], 20, fill=True)
            c.setFillColor(colors.black)
            c.drawString(x + sum(largura_colunas_gastos[:j]) + 5, y_gastos - (i + 1) * 20 + 5, str(dados[j]))

    novoSaldo = saldo - saida

    c.setFont("Helvetica-Bold", 15)

    c.setFillColorRGB(0, 0, 0)
    c.drawString(x, 800, "Saldo Atual:  ")
    c.setFillColorRGB(221 / 255, 147 / 255, 0)
    c.drawString(x + 90, 800, f" R${saldo}")

    c.setFillColorRGB(0, 0, 0) 
    c.drawString(x, 775, "Saída Prevista:   ")
    c.setFillColorRGB(220 / 255, 0, 0)
    c.drawString(x + 105, 775, f"  R${saida}")

    c.setFillColorRGB(0, 0, 0)
    c.drawString(x, 750, "Saldo Restante: ")
    c.setFillColorRGB(0, 129 / 255, 0)
    c.drawString(x + 120, 750, f"R${novoSaldo}")

    data_atual = datetime.now().strftime("%d-%m-%y")

    nome_pdf = f"financeiroIBF{data_atual}.pdf"

    desktop_path = os.path.expanduser("~/Desktop")
    pdf_path = os.path.join(desktop_path, nome_pdf)
    contador = 1
    while os.path.exists(pdf_path):
        nome_pdf = f"financeiroIBF{data_atual} ({contador}).pdf"
        pdf_path = os.path.join(desktop_path, nome_pdf)
        contador += 1

    c.save()

    os.rename("financeiroIBF.pdf", pdf_path)

def consultarPlanilha():
    definirSaida()
    definirSaldo()
    consultarPlanilha.show()
    cursor = conexao.cursor()
    comandoSQLColab = 'SELECT nome, cargo, segmento, valor FROM colaboradores ORDER BY segmento ASC, valor DESC'

    cursor.execute(comandoSQLColab)
    leituraBancoColab = cursor.fetchall()

    consultarPlanilha.tblColabPlanilha.setRowCount(len(leituraBancoColab))
    consultarPlanilha.tblColabPlanilha.setColumnCount(4)

    for i in range(0, len(leituraBancoColab)):
        for j in range(0, 4):
            consultarPlanilha.tblColabPlanilha.setItem(i, j, QtWidgets.QTableWidgetItem(str(leituraBancoColab[i][j])))

    comandoSQLGastos = 'SELECT descricao, quantia FROM gastos'
    cursor.execute(comandoSQLGastos)
    leituraBancoGastos = cursor.fetchall()

    consultarPlanilha.tblConsultarGastos.setRowCount(len(leituraBancoGastos))
    consultarPlanilha.tblConsultarGastos.setColumnCount(2)

    for i in range(0, len(leituraBancoGastos)):
        for j in range(0,2):
            consultarPlanilha.tblConsultarGastos.setItem(i, j, QtWidgets.QTableWidgetItem(str(leituraBancoGastos[i][j])))
    
    # as duas tabelas prontas acima ↑

    novoSaldo = saldo - saida

    consultarPlanilha.lblSaldo.setText(str(saldo))
    consultarPlanilha.lblSaida.setText(str(saida))
    consultarPlanilha.lblNovoSaldo.setText(str(novoSaldo))

    if not hasattr(consultarPlanilha, 'gerar_pdf_conectado'):
        consultarPlanilha.gerar_pdf_conectado = False

    if not consultarPlanilha.gerar_pdf_conectado:
        consultarPlanilha.btnGerarPdf.clicked.connect(gerar_pdf)
        consultarPlanilha.gerar_pdf_conectado = True

def realizarPagamentos():
    if not hasattr(realizarPagamentos, 'msg_box_executada') or not realizarPagamentos.msg_box_executada:
        dialog = QMessageBox(consultarCaixa)
        dialog.setText('Essa ação fará com que feche o mês e exclua os registros de gastos. \n Ação irreversível! Tem certeza?')
        dialog.setWindowTitle('CUIDADO!')
        dialog.setIcon(QMessageBox.Warning)
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        resposta = dialog.exec_()

        if resposta != QMessageBox.Ok:
            return 

        realizarPagamentos.msg_box_executada = True

    dialog = QMessageBox(consultarCaixa)
    dialog.setText('Para maior segurança, o programa deverá ser reaberto.')
    dialog.setWindowTitle('IMPORTANTE!')
    dialog.setIcon(QMessageBox.Information)
    dialog.setStandardButtons(QMessageBox.Ok)
    resposta = dialog.exec_()

    cursor = conexao.cursor()
    cursor.execute('DELETE FROM gastos')
    conexao.commit()

    global saldo, saida
    novoSaldo = saldo - saida
    cursor.execute("UPDATE caixa SET caixa = ? WHERE ID = 1", (novoSaldo,))
    conexao.commit()
    consultarCaixa.close()
    main.close()

def consultarCaixa():
    definirSaida()
    definirSaldo()
    consultarCaixa.show()
    consultarCaixa.lblSaida.setText(str(saida))
    global saldo
    consultarCaixa.lblSaldo.setText(str(saldo))
    consultarCaixa.txtEntrada.setText('')
    novoSaldo = saldo - saida
    consultarCaixa.lblNovoSaldo.setText(str(novoSaldo))
    
    consultarCaixa.btnAddSaldo.clicked.connect(atualizarSaldo)
    consultarCaixa.btnPagamento.clicked.connect(realizarPagamentos)

consultarCaixa.msg_box_executada = False

def atualizarSaldo():
    entrada = float(consultarCaixa.txtEntrada.text())
    global  saldo
    saldo += entrada
    cursor = conexao.cursor()
    cursor.execute("UPDATE caixa SET caixa = ? WHERE ID = 1", (saldo,))
    conexao.commit()

    dialog = QMessageBox(consultarCaixa)
    dialog.setText(' Saldo atualizado com sucesso! \n\n Para implementar a mudança\n abra a janela novamente.')
    dialog.setWindowTitle('IMPORTANTE!')
    dialog.setIcon(QMessageBox.Information)
    dialog.setStandardButtons(QMessageBox.Ok)
    resposta = dialog.exec_()

    if resposta == QMessageBox.Ok:
        consultarCaixa.close()
        consultarCaixa.btnAddSaldo.clicked.disconnect(atualizarSaldo)

def definirSaida():
    global saida
    cursor = conexao.cursor()

    cursor.execute("SELECT SUM(valor) FROM colaboradores")
    soma_colaboradores = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(quantia) FROM gastos")
    resultado_gastos = cursor.fetchone()
    soma_gastos = resultado_gastos[0] if resultado_gastos[0] is not None else 0
    saida = soma_colaboradores + soma_gastos

def definirSaldo():
     global saldo
     cursor = conexao.cursor()
     cursor.execute('SELECT * FROM caixa')
     leituraBanco = cursor.fetchall()
     saldo = leituraBanco[0][1]

def excluirGastos():
    dialog = QMessageBox(consultarGastos)
    dialog.setText('Essa ação excluirá o registro\n         e é irreversível!')
    dialog.setWindowTitle('CUIDADO!')
    dialog.setIcon(QMessageBox.Warning)
    dialog.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
    resposta = dialog.exec_()

    if resposta == QMessageBox.Ok:
        
        remover = consultarGastos.tblConsultarGastos.currentRow()
        consultarGastos.tblConsultarGastos.removeRow(remover)

        cursor = conexao.cursor()
        cursor.execute('SELECT ID FROM gastos')
        leituraBanco = cursor.fetchall()
        ValorID = leituraBanco[remover][0]

        cursor.execute('DELETE FROM gastos WHERE ID='+str(ValorID))
        
        conexao.commit()
        consultarGastos.close()

def editarGastos():

    global numeroIDgastos
    dados = consultarGastos.tblConsultarGastos.currentRow()
    cursor = conexao.cursor()
    cursor.execute('SELECT ID FROM gastos')
    leituraBanco = cursor.fetchall()
    valorID = leituraBanco[dados][0]
    cursor.execute('SELECT * FROM gastos WHERE ID ='+str(valorID))
    leituraBanco = cursor.fetchall()

    editarGastos.show()
    numeroIDgastos = valorID

    editarGastos.txtEditDesc.setPlainText(str(leituraBanco[0][1]))
    editarGastos.txtEditQuantia.setText(str(leituraBanco[0][2]))

def salvarEdicaoGastos():
    global numeroIDgastos

    descricaoEdit = editarGastos.txtEditDesc.toPlainText()
    quantiaEdit = editarGastos.txtEditQuantia.text()

    cursor = conexao.cursor()
    cursor.execute("UPDATE gastos SET descricao='{}', quantia='{}' WHERE ID={}".format(descricaoEdit, quantiaEdit, numeroIDgastos))

    editarGastos.close()
    consultarGastos.close()

    conexao.commit()

def consultarGastos():
    consultarGastos.show()

    cursor = conexao.cursor()
    comandoSQL = 'SELECT descricao, quantia FROM gastos'
    cursor.execute(comandoSQL)
    leituraBanco = cursor.fetchall()

    consultarGastos.tblConsultarGastos.setRowCount(len(leituraBanco))
    consultarGastos.tblConsultarGastos.setColumnCount(2)

    for i in range(0, len(leituraBanco)):
        for j in range(0,2):
            consultarGastos.tblConsultarGastos.setItem(i, j, QtWidgets.QTableWidgetItem(str(leituraBanco[i][j])))

def inserirGastos():
    descricao = addGastos.txtDescricao.toPlainText()
    quantia = addGastos.txtQuantia.text()

    cursor = conexao.cursor()
    comandoSQL = 'INSERT INTO gastos (descricao, quantia) VALUES (?, ?)'
    dados = (str(descricao), str(quantia))
    cursor.execute(comandoSQL, dados)
    conexao.commit()

    addGastos.txtDescricao.setPlainText('')
    addGastos.txtQuantia.setText('')

def addGastos():
    addGastos.show()

def excluirColab():
    dialog = QMessageBox(consultarColab)
    dialog.setText('Essa ação excluirá o registro\n         e é irreversível!')
    dialog.setWindowTitle('CUIDADO!')
    dialog.setIcon(QMessageBox.Warning)
    dialog.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
    resposta = dialog.exec_()

    if resposta == QMessageBox.Ok:
        
        remover = consultarColab.tblColab.currentRow()
        consultarColab.tblColab.removeRow(remover)

        cursor = conexao.cursor()
        cursor.execute('SELECT ID FROM colaboradores')
        leituraBanco = cursor.fetchall()
        valorID = leituraBanco[remover][0]

        cursor.execute('DELETE FROM colaboradores WHERE ID='+str(valorID))

        conexao.commit()
        consultarColab.close()

def editarColab():
    global numeroIDcolab
    dados = consultarColab.tblColab.currentRow()

    cursor = conexao.cursor()
    cursor.execute('SELECT ID FROM colaboradores')
    leituraBanco = cursor.fetchall()
    valorID = leituraBanco[dados][0]
    cursor.execute('SELECT * FROM colaboradores WHERE ID ='+str(valorID))
    leituraBanco = cursor.fetchall()
    
    editarColab.show()
    numeroIDcolab = valorID

    editarColab.txtEditarColab.setText(str(leituraBanco[0][1]))
    editarColab.txtEditarCargo.setText(str(leituraBanco[0][2]))
    editarColab.txtEditarSegmento.setText(str(leituraBanco[0][3]))
    editarColab.txtEditarValor.setText(str(leituraBanco[0][4]))

def salvarEdicaoColab():
    global numeroIDcolab

    dialog = QMessageBox(consultarColab)
    dialog.setText(' Cadastro atualizado com sucesso! \n\n Para implementar a mudança\n abra a janela novamente.')
    dialog.setWindowTitle('IMPORTANTE!')
    dialog.setIcon(QMessageBox.Information)
    dialog.setStandardButtons(QMessageBox.Ok)
    resposta = dialog.exec_()

    if resposta == QMessageBox.Ok:

        nomeEdit = editarColab.txtEditarColab.text()
        cargoEdit = editarColab.txtEditarCargo.text()
        segmentoEdit = editarColab.txtEditarSegmento.text()
        valorEdit = editarColab.txtEditarValor.text()

        cursor = conexao.cursor()
        cursor.execute("UPDATE colaboradores SET nome='{}', cargo='{}', segmento='{}', valor='{}' WHERE ID={}".format( nomeEdit, cargoEdit, segmentoEdit, valorEdit, numeroIDcolab))

        editarColab.close()
        consultarColab.close()
        conexao.commit()

def consultarColab():
    consultarColab.show()
    cursor = conexao.cursor()
    comandoSQL = 'SELECT nome, cargo, segmento, valor FROM colaboradores'
    cursor.execute(comandoSQL)
    leituraBanco = cursor.fetchall()

    consultarColab.tblColab.setRowCount(len(leituraBanco))
    consultarColab.tblColab.setColumnCount(4)

    for i in range(0, len(leituraBanco)):
        for j in range(0, 4):
            consultarColab.tblColab.setItem(i, j, QtWidgets.QTableWidgetItem(str(leituraBanco[i][j])))

def inserirColaborador():
    nome = main.txtAddColab.text().title()
    cargo = main.txtAddCargo.text().title()
    segmento = main.txtAddSegmento.text().title()
    valor = main.txtAddValor.text()

    cursor = conexao.cursor()
    comandoSQL = 'INSERT INTO colaboradores (nome, cargo, segmento, valor) VALUES (?, ?, ?, ?)'
    dados = (str(nome), str(cargo), str(segmento), str(valor))
    cursor.execute(comandoSQL, dados)
    conexao.commit()

    main.txtAddColab.setText('')
    main.txtAddCargo.setText('')
    main.txtAddSegmento.setText('')
    main.txtAddValor.setText('')

app = QtWidgets.QApplication([])
main = uic.loadUi("main.ui")
main.setWindowTitle("Financeiro IBF")
main.btnAddCadastro.clicked.connect(inserirColaborador)
main.btnConsultarColab.clicked.connect(consultarColab)
main.btnGastosExtras.clicked.connect(addGastos)
main.btnCaixa.clicked.connect(consultarCaixa)
main.btnPlanilha.clicked.connect(consultarPlanilha)

consultarColab = uic.loadUi('ConsultarColab.ui')
consultarColab.setWindowTitle("Financeiro IBF - Consultar Colaborador")
consultarColab.btnEditColab.clicked.connect(editarColab)
consultarColab.btnExcluirColab.clicked.connect(excluirColab)

editarColab = uic.loadUi('editarColab.ui')
editarColab.setWindowTitle("Financeiro IBF - Editar Colaborador")
editarColab.btnConfirmarEdit.clicked.connect(salvarEdicaoColab)

addGastos = uic.loadUi('addGastos.ui')
addGastos.setWindowTitle("Financeiro IBF - Adicionar Gastos")
addGastos.btnConfirmarGastos.clicked.connect(inserirGastos)
addGastos.btnConsultarGastos.clicked.connect(consultarGastos)

consultarGastos = uic.loadUi('consultarGastos.ui')
consultarGastos.setWindowTitle("Financeiro IBF - Consultar Gastos")
consultarGastos.btnEditarGastos.clicked.connect(editarGastos)
consultarGastos.btnExcluirGastos.clicked.connect(excluirGastos)

editarGastos = uic.loadUi('editarGastos.ui')
editarGastos.setWindowTitle("Financeiro IBF - Editar Gastos")
editarGastos.btnSalvarEdit.clicked.connect(salvarEdicaoGastos)

consultarCaixa = uic.loadUi('consultarCaixa.ui')
consultarCaixa.setWindowTitle("Financeiro IBF - Consultar Caixa")

consultarPlanilha = uic.loadUi('consultarPlanilha.ui')
consultarPlanilha.setWindowTitle("Financeiro IBF - Consultar Planilha")

main.show()
app.exec()