from django.shortcuts import render
from django.http import HttpResponse
import ast
import matplotlib.pyplot as plt
from io import BytesIO
import networkx as nx

# Vista principal que muestra la calculadora
def index(request):
    return render(request, 'calc/index.html')

# Vista que genera el árbol sintáctico
def generate_tree(request):
    expression = request.GET.get('expression', '')  # Obtener la expresión desde el query string
    if not expression:
        return HttpResponse("No se proporcionó una expresión.", status=400)

    try:
        tree = ast.parse(expression, mode='eval')
        img = create_tree_image(tree.body)
        return HttpResponse(img, content_type="image/png")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=400)

# Función para generar el gráfico del árbol AST
def create_tree_image(node):
    graph = nx.DiGraph()
    counter = [0]

    def add_edges(node, parent=None):
        current_id = f"node{counter[0]}"
        counter[0] += 1

        # Asignar la etiqueta correcta al nodo
        if isinstance(node, ast.BinOp):
            label = {
                ast.Add: '+',
                ast.Sub: '-',
                ast.Mult: '*',
                ast.Div: '/',
            }.get(type(node.op), '?')  # Usar '?' si no se reconoce el operador
        elif isinstance(node, ast.Constant):  # Para Python >=3.8
            label = str(node.value)
        elif isinstance(node, ast.Num):  # Para Python <3.8
            label = str(node.n)
        else:
            label = "Unknown"

        graph.add_node(current_id, label=label)

        if parent:
            graph.add_edge(parent, current_id)

        if isinstance(node, ast.BinOp):
            add_edges(node.left, current_id)
            add_edges(node.right, current_id)

    add_edges(node)

    # Crear el diseño del árbol
    pos = nx.spring_layout(graph)  # Diseño alternativo sin Graphviz
    labels = nx.get_node_attributes(graph, 'label')

    # Configurar la visualización con matplotlib
    plt.figure(figsize=(6, 4), facecolor='#333333')  # Fondo oscuro
    nx.draw(
        graph, pos,
        labels=labels,
        with_labels=True,
        node_size=2000,
        node_color='#FFFFFF',  # Fondo de los nodos blanco
        font_size=10,
        font_color='#000000',  # Texto negro
        edge_color='#FFFFFF',  # Líneas blancas
    )
    plt.title("Árbol Sintáctico", color="white", fontsize=16, pad=20)
    plt.axis("off")  # Ocultar los ejes

    # Guardar el gráfico como imagen
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches='tight', facecolor='#333333')
    plt.close()
    buffer.seek(0)
    return buffer.getvalue()
