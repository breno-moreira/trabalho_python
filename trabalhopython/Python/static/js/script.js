const modalCadastro = new bootstrap.Modal(document.getElementById('modalcadastro'));

function novo(){
    document.getElementById("titulo").value = "";
    document.getElementById("artista").value = ""; 
    document.getElementById("ano").value = "";
    document.getElementById("genero").value = "";
    document.getElementById("idmusica").value = "";
    modalCadastro.show();
}

function salvar() {
    const titulo = document.getElementById("titulo").value.trim();
    const artista = document.getElementById("artista").value.trim();
    const ano = document.getElementById("ano").value.trim();
    const genero = document.getElementById("genero").value.trim();
    const id = document.getElementById("idmusica").value.trim();

    if (!titulo || !artista || !ano || !genero) {
        alert("Preencha todos os campos!");
        return;
    }

    const musicas = {
        idmusica: id,
        titulo: titulo,
        artista: artista,
        ano: ano,
        genero: genero
    };

    let url = "http://127.0.0.1:3333/musica";
    let method = "POST";

    if (id) {
        url += "/" + id;
        method = "PUT";
    }

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(musicas)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao salvar sua musica");
        }
        return response.text();  
    })
    .then(() => {
        listar();
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalcadastro'));
        modal.hide();  
    })
    .catch(error => {
        console.error("Erro ao salvar sua musica:", error);
    });
}

function editar(id){    
    fetch("http://127.0.0.1:3333/musica/" + id)
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao buscar a musica");
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("titulo").value = data.titulo;
        document.getElementById("artista").value = data.artista;
        document.getElementById("ano").value = data.ano;
        document.getElementById("genero").value = data.genero;
        document.getElementById("idmusica").value = data.idmusica;
        modalCadastro.show();
    })
    .catch(error => {
        console.error("Erro ao buscar a musica:", error);
    });
}

function listar(){
    const lista = document.getElementById("lista");
    lista.innerHTML = "<tr><td colspan='6' class='text-center'>Carregando...</td></tr>";
    
    fetch("http://127.0.0.1:3333/musica")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao buscar musicas");
            }
            return response.json();
        })
        .then(dados => mostrar(dados))
        .catch(error => {
            lista.innerHTML = `<tr><td colspan='6' class='text-danger text-center'>Erro ao carregar suas musicas</td></tr>`;
            console.error("Erro ao listar as musicas:", error);
        });
}

function excluir(id){
    fetch("http://127.0.0.1:3333/musica/" + id, {
        method: "DELETE"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao excluir a musica");
        }
        return response.text();
    })
    .then(() => {
        listar();
    })
    .catch(error => {
        console.error("Erro ao excluir a musica:", error);
    });
}

function mostrar(dados){
    const lista = document.getElementById("lista");
    lista.innerHTML = "";
    for(let i = 0; i < dados.length; i++){
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${dados[i].idmusica}</td>
            <td>${dados[i].titulo}</td>
            <td>${dados[i].artista}</td>
            <td>${dados[i].ano}</td>
            <td>${dados[i].genero}</td>
            <td>
                <button onclick='editar(${dados[i].idmusica})'><img src='imgs/edit.svg'></button>
                <button onclick='excluir(${dados[i].idmusica})'><img src='imgs/x-square.svg'></button>
            </td> `;
        lista.appendChild(tr);
    }
}

listar();