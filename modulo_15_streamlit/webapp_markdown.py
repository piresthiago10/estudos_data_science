import streamlit as st


def main():
    st.title("Exemplos de Markdown com Streamlit")

    st.header("1. Títulos:")
    st.markdown("# Título de Nível 1")
    st.markdown("## Título de Nível 2")
    st.markdown("### Título de Nível 3")

    st.header("2. Texto em negrito e itálico:")
    st.markdown("**Texto em negrito** e *texto em itálico*.")

    st.header("3. Listas:")
    st.markdown("- Item 1 :sunglasses:")
    st.markdown("- Item 2 :100:")
    st.markdown("- Item 3 :ok_hand:")

    st.header("4. Links:")
    st.markdown("[Texto do Link](https://www.exemplo.com)")

    st.header("5. Imagens:")
    st.image("https://media3.giphy.com/media/12i3TW7x8vp7sQ/giphy.gif?cid=6c09b952n6uv9ekhvriigss3lzbzsh6ugq7xmklt5ply8pms&ep=v1_gifs_search&rid=giphy.gif&ct=g")

    st.header("6. Código em linha:")
    st.markdown("`código em linha`")

    st.header("7. Blocos de código:")
    st.code("""
            bloco de código
        """)

    st.header("8. Citações:")
    st.markdown("> Isso é uma citação.")

    st.header("9. Linhas horizontais:")
    st.markdown("---")

    st.header("10. Tabela:")
    st.markdown("""
    | Coluna 1 | Coluna 2 | Coluna 3 |
    |----------|----------|----------|
    | Valor 1  | Valor 2  | Valor 3  |
    | Valor 4  | Valor 5  | Valor 6  |
    """)

    st.header("Markdown com HTML:")
    st.markdown("""
    <div style="background-color: lightblue; padding: 10px;">
        <p style="font-size: 20px; color: red;">Este é um exemplo de Markdown com HTML.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
