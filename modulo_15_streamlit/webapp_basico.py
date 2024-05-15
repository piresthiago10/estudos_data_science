import streamlit as st
import plotly.graph_objects as go

def example_basic():
    st.title("Streamlit Exemplos Básicos")
    st.header("Textos")
    st.write("Este é um exemplo de texto.")
    st.subheader("Títulos")
    st.write("# Este é um título de nível 1")
    st.write("## Este é um título de nível 2")
    st.write("### Este é um título de nível 3")
    st.header("Widgets")
    st.subheader("Checkbox")
    if st.checkbox("Mostrar/Ocultar"):
        st.write("Este é um exemplo de checkbox.")
    st.subheader("Selectbox")
    option = st.selectbox("Selecione uma opção", ["Opção 1", "Opção 2", "Opção 3"])
    st.write(f"Você selecionou: {option}")

def example_advanced():
    st.title("Streamlit Exemplos Avançados")
    st.header("Gráficos")
    st.subheader("Gráfico de Linhas")
    st.line_chart({"dados": [1, 2, 3, 4, 5, 3, 3 ,8]})
    st.subheader("Gráfico de Barras")
    st.bar_chart({"dados": [5, 4, 3, 2, 1]})
    st.subheader("Mapa de Calor")
    heatmap_data = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    fig = go.Figure(data=go.Heatmap(z=heatmap_data))
    st.plotly_chart(fig)

def main():
    st.sidebar.title("Menu")
    example_options = ["Exemplos Básicos", "Exemplos Avançados"]
    example_choice = st.sidebar.radio("Escolha um exemplo", example_options)

    if example_choice == "Exemplos Básicos":
        example_basic()
    elif example_choice == "Exemplos Avançados":
        example_advanced()

if __name__ == "__main__":
    main()
