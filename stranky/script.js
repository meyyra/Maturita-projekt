document.addEventListener("DOMContentLoaded", function () {
    fetchCategories();
});
// získání kategorií z databáze a vykreslení tlačítek
function fetchCategories() {
    fetch("http://127.0.0.1:5000/categories")
        .then(response => response.json())
        .then(categories => {
            const categoriesDiv = document.getElementById("categories");
            categoriesDiv.innerHTML = "";
            categories.forEach(category => {
                const button = document.createElement("button");
                button.textContent = category[1];
                button.classList.add("category-button");  // Přidá třídu pro stylování
                button.onclick = () => fetchProducts(category[0]);
                categoriesDiv.appendChild(button);
            });
        })
        .catch(error => console.error("Chyba při načítání kategorií:", error));
}
// získání produktů z databáze
function fetchProducts(categoryId) {
    fetch(`http://127.0.0.1:5000/products/${categoryId}`)
        .then(response => response.json())
        .then(products => {
            const productsDiv = document.getElementById("products");
            productsDiv.innerHTML = "";
            products.forEach(product => {
                const productDiv = document.createElement("div");
                productDiv.textContent = `${product[0]} - ${product[1]} Kč`;
                productsDiv.classList.add("product");  // Přidá třídu pro stylování
                productsDiv.appendChild(productDiv);
            });
        })
        .catch(error => console.error("Chyba při načítání produktů:", error));
}


