let slideIndex = 0;
// efekt pro galerii obrázků
function showSlides() {
    let slides = document.getElementsByClassName("slide");

    // Skryjeme všechny obrázky
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    // Posuneme se na další slide
    slideIndex++;

    // Když dojedeme na konec, začneme znovu
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }

    // Ukážeme aktuální slide
    slides[slideIndex - 1].style.display = "block";

    // Spustíme znovu každé 3 sekundy
    setTimeout(showSlides, 3000);
}

// Spustíme slider hned po načtení
showSlides();
// funkce pro odhlášení
function logout() {
    modalTitle.textContent = "Odhlášeno!";
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("logincontent").style.display = "none";
    document.getElementById("userName").textContent = "";
    document.getElementById("userPoints").textContent = ""; // Vyčistíme body
}

// login menu
document.addEventListener("DOMContentLoaded", () => {
    const giftIcon = document.querySelector('.socky .soc[src="./ikony/gift.png"]');
    const loginModal = document.getElementById("loginModal");
    const closeModal = document.querySelector(".close");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const modalTitle = document.getElementById("modalTitle");
    const toggleForm = document.getElementById("toggleForm");

    // Otevření modálního okna pod dárečkem
    giftIcon.addEventListener("click", (e) => {
        e.preventDefault();
        const iconRect = giftIcon.getBoundingClientRect();
        loginModal.style.top = `${iconRect.bottom + window.scrollY}px`;
        loginModal.style.left = `${iconRect.left + window.scrollX}px`;
        loginModal.style.display = "block";
    });

    // Zavření modálního okna
    closeModal.addEventListener("click", () => {
        loginModal.style.display = "none";
    });

    // Zavření okna kliknutím mimo
    window.addEventListener("click", (e) => {
        if (e.target === loginModal) {
            loginModal.style.display = "none";
        }
    });

    // Přepínání mezi přihlášením a registrací
    toggleForm.addEventListener("click", (e) => {
        e.preventDefault();
        if (loginForm.style.display === "none") {
            loginForm.style.display = "block";
            registerForm.style.display = "none";
            modalTitle.textContent = "Přihlášení";
            toggleForm.innerHTML = 'Nemáš účet? <a href="#">Registruj se!</a>';
        } else {
            loginForm.style.display = "none";
            registerForm.style.display = "block";
            modalTitle.textContent = "Registrace";
            toggleForm.innerHTML = 'Máš už účet? <a href="#">Přihlaš se!</a>';
        }
    });

    // Odeslání přihlašovacího formuláře
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
    
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
    
        const response = await fetch("login.php", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
    
        const data = await response.json();
    
        if (data.success) {

            // Zobrazíme body v modalu
            modalTitle.textContent = "Přihlášeno!";
            document.getElementById("loginForm").style.display = "none";
            document.getElementById("logincontent").style.display = "block";
            document.getElementById("userName").textContent = `${data.username}`
            document.getElementById("userPoints").textContent = `Vaše body: ${data.points}`;
        } else {
            alert(data.message || "Přihlášení se nezdařilo.");
        }
    });
    

    // Odeslání registračního formuláře
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const newUsername = document.getElementById("newUsername").value;
        const newPassword = document.getElementById("newPassword").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (newPassword !== confirmPassword) {
            alert("Hesla se neshodují!");
            return;
        }

        const response = await fetch("register.php", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: newUsername, password: newPassword })
        });

        const data = await response.json();
        if (data.success) {
            alert("Registrace úspěšná!");
            toggleForm.click(); // přepne zpět na přihlášení
        } else {
            alert("Registrace se nezdařila: " + data.error);
        }
    });
});

const reservationBtn = document.getElementById("rezervace");
const modal = document.getElementById("rezmodal");
const closeBtn = document.querySelector(".close");
const copyButton = document.getElementById("copyButton");
const phoneNumber = document.getElementById("phoneNumber").textContent;

reservationBtn.onclick = () => modal.style.display = "flex";
closeBtn.onclick = () => modal.style.display = "none";
window.onclick = (event) => {
    if (event.target === modal) modal.style.display = "none";
};

copyButton.onclick = () => {
    navigator.clipboard.writeText(phoneNumber);
    alert("Telefonní číslo zkopírováno!");
};
