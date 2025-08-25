document.addEventListener('DOMContentLoaded', function() {
    // Elementos de UI
    const tableBody = document.getElementById('productTableBody');
    const searchInput = document.getElementById('searchInput');
    const brandFiltersContainer = document.getElementById('brandFilters');
    const verticalFiltersContainer = document.getElementById('verticalFilters');

    const stockHeader = document.getElementById('stockHeader');
    const stockArrow = document.getElementById('stockArrow');

    // Login UI
    const loginOverlay = document.getElementById('loginOverlay');
    const loginButton = document.getElementById('loginButton');
    const loginEmail = document.getElementById('loginEmail');
    const loginPassword = document.getElementById('loginPassword');
    const loginError = document.getElementById('loginError');

    let allProducts = [];
    let activeBrand = 'all';
    let activeVertical = 'all';
    let stockSortOrder = null; // null, 'asc', 'desc'

    // --- Renderização da tabela ---
    function renderTable(products) {
        tableBody.innerHTML = '';

        if (products.length === 0) {
            const row = tableBody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 5;
            cell.textContent = 'Nenhum produto encontrado.';
            cell.style.textAlign = 'center';
            cell.style.padding = '20px';
        } else {
            products.forEach(product => {
                const row = tableBody.insertRow();
                row.insertCell().textContent = product.NOME || 'N/A';
                row.insertCell().textContent = product.Id || 'N/A';
                row.insertCell().textContent = product.MARCA || 'N/A';
                row.insertCell().textContent = product.VERTICAL || 'N/A';
                
                const stockCell = row.insertCell();
                const stock = parseInt(product.ESTOQUE, 10);
                stockCell.textContent = isNaN(stock) ? '0' : stock;

                if (stock < 5) {
                    stockCell.classList.add('stock-low');
                    stockCell.textContent = `⚠️ ${stock}`;
                }
            });
        }
    }

    // --- Lógica combinada de filtros e ordenação ---
    function applyFiltersAndSort() {
        const searchTerm = searchInput.value.toLowerCase();

        let filteredProducts = allProducts.filter(p => {
            const matchesSearch = searchTerm ? 
                (p.NOME || '').toLowerCase().includes(searchTerm) ||
                (p.MARCA || '').toLowerCase().includes(searchTerm) ||
                (p.VERTICAL || '').toLowerCase().includes(searchTerm)
                : true;

            const brand = p.MARCA || '';
            const vertical = p.VERTICAL || '';
            const matchesBrand = activeBrand === 'all' || brand === activeBrand;
            const matchesVertical = activeVertical === 'all' || vertical === activeVertical;

            return matchesSearch && matchesBrand && matchesVertical;
        });
        
        if (stockSortOrder === 'asc') {
            filteredProducts.sort((a, b) => (parseInt(a.ESTOQUE, 10) || 0) - (parseInt(b.ESTOQUE, 10) || 0));
        } else if (stockSortOrder === 'desc') {
            filteredProducts.sort((a, b) => (parseInt(b.ESTOQUE, 10) || 0) - (parseInt(a.ESTOQUE, 10) || 0));
        }

        renderTable(filteredProducts);
    }

    function createFilterButtons(container, items, filterType) {
        container.innerHTML = '<button class="active" data-filter="all">Todas</button>';
        items.forEach(item => {
            if (item) {
                const button = document.createElement('button');
                button.textContent = item;
                button.dataset.filter = item;
                container.appendChild(button);
            }
        });

        container.addEventListener('click', function(e) {
            if (e.target.tagName === 'BUTTON') {
                const filterValue = e.target.dataset.filter;
                if (filterType === 'brand') activeBrand = filterValue;
                else if (filterType === 'vertical') activeVertical = filterValue;

                container.querySelector('.active').classList.remove('active');
                e.target.classList.add('active');
                applyFiltersAndSort();
            }
        });
    }

    // --- inicialização do app (carrega produtos / monta filtros) ---
    async function initializeApp() {
        try {
            const response = await fetch('/api/products');
            if (!response.ok) throw new Error(`Erro na rede: ${response.statusText}`);
            
            allProducts = await response.json();

            const uniqueBrands = [...new Set(allProducts.map(p => p.MARCA))].sort();
            const uniqueVerticals = [...new Set(allProducts.map(p => p.VERTICAL))].sort();

            createFilterButtons(brandFiltersContainer, uniqueBrands, 'brand');
            createFilterButtons(verticalFiltersContainer, uniqueVerticals, 'vertical');
            
            searchInput.addEventListener('input', applyFiltersAndSort);

            stockHeader.addEventListener('click', () => {
                if (stockSortOrder === 'asc') {
                    stockSortOrder = 'desc';
                    stockArrow.textContent = '↓';
                } else if (stockSortOrder === 'desc') {
                    stockSortOrder = null;
                    stockArrow.textContent = '↕';
                } else {
                    stockSortOrder = 'asc';
                    stockArrow.textContent = '↑';
                }
                applyFiltersAndSort();
            });

            applyFiltersAndSort();
        } catch (error) {
            console.error('Falha ao carregar os dados dos produtos:', error);
            tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:red;">Erro ao carregar os dados.</td></tr>`;
        }
    }

    // --- Login handling ---
    async function attemptLogin() {
        loginError.textContent = '';
        const email = loginEmail.value.trim();
        const password = loginPassword.value;

        if (!email || !password) {
            loginError.textContent = 'Preencha e-mail e senha.';
            return;
        }

        loginButton.disabled = true;
        loginButton.textContent = 'Entrando...';

        try {
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (res.ok && data.success) {
                // Sucesso: esconder modal e inicializar app
                loginOverlay.style.display = 'none';
                initializeApp();
            } else {
                loginError.textContent = data.message || 'Credenciais inválidas.';
            }
        } catch (err) {
            console.error('Erro no login:', err);
            loginError.textContent = 'Erro de rede ao tentar autenticar.';
        } finally {
            loginButton.disabled = false;
            loginButton.textContent = 'Entrar';
        }
    }

    // Eventos do modal (botão e Enter)
    loginButton.addEventListener('click', attemptLogin);
    [loginEmail, loginPassword].forEach(el => {
        el.addEventListener('keydown', (ev) => {
            if (ev.key === 'Enter') attemptLogin();
        });
    });
    let selectedOption = null;

    // Abre/fecha menu engrenagem
    function toggleSettingsMenu() {
    document.getElementById("settingsMenu").classList.toggle("hidden");
    }

    // Abrir modal senha
    function openPasswordModal(option) {
    selectedOption = option;
    document.getElementById("passwordModal").classList.remove("hidden");
    }

    // Fechar modal senha
    function closePasswordModal() {
    document.getElementById("passwordModal").classList.add("hidden");
    document.getElementById("adminPassword").value = "";
    document.getElementById("passwordError").innerText = "";
    }

    // Verificar senha
    function checkPassword() {
    const input = document.getElementById("adminPassword").value;
    if (input === "SenhaForte10@") {
        closePasswordModal();
        if (selectedOption === "gerenciamento") {
        openGerenciamento();
        }
    } else {
        document.getElementById("passwordError").innerText = "Senha incorreta!";
    }
    }

    // Abrir tela gerenciamento
    async function openGerenciamento() {
    const resp = await fetch("/get-auth-file");
    const text = await resp.text();
    document.getElementById("authContent").value = text;
    document.getElementById("gerenciamentoScreen").classList.remove("hidden");
    }

    // Fechar tela gerenciamento
    function closeGerenciamento() {
    document.getElementById("gerenciamentoScreen").classList.add("hidden");
    }

    // Salvar alterações no auth.csv
    async function saveAuthFile() {
    const content = document.getElementById("authContent").value;
    const resp = await fetch("/save-auth-file", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content })
    });

    if (resp.ok) {
        alert("Arquivo salvo com sucesso!");
    } else {
        alert("Erro ao salvar!");
    }
    }

    // Observação: não chamamos initializeApp aqui — só após login bem-sucedido
});
