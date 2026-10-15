const nameInput = document.getElementById("nameInput");
const passwordInput = document.getElementById("passwordInput");
const submitBtn = document.getElementById("submitBtn");
const toggleMode = document.getElementById("toggleMode");
const formTitle = document.getElementById("formTitle");
const switchMode = document.getElementById("switchMode");
const welcomeText = document.getElementById("welcomeText");
const welcomeArea = document.getElementById("welcomeArea");
const authArea = document.getElementById("authArea");
const logout = document.getElementById("logout");
const activeUser = localStorage.getItem("currentUser");

if (activeUser) {
  showWelcome(activeUser);
}

let isLoginMode = true;

function toggleFormMode() {
  isLoginMode = !isLoginMode;
  formTitle.textContent = isLoginMode ? "Anmelden" : "Registrieren";
  submitBtn.textContent = isLoginMode ? "Anmelden" : "Registrieren";
  switchMode.innerHTML = isLoginMode
    ? 'Noch keinen Account? <a href="#" id="toggleMode">Registrieren</a>'
    : 'Schon registriert? <a href="#" id="toggleMode">Anmelden</a>';

  document.getElementById("toggleMode").addEventListener("click", (e) => {
    e.preventDefault();
    toggleFormMode();
  });
}

function handleSubmit() {
  const name = nameInput.value.trim();
  const password = passwordInput.value.trim();

  if (!name || !password) {
    alert("Bitte Benutzername und Passwort eingeben.");
    return;
  }

  const users = JSON.parse(localStorage.getItem("users") || "{}");

  if (isLoginMode) {
    if (!users[name] || users[name] !== password) {
      alert("Falscher Benutzername oder Passwort.");
      return;
    }
    showWelcome(name);
  } else {
    if (users[name]) {
      alert("Benutzername bereits vergeben.");
      return;
    }
    users[name] = password;
    localStorage.setItem("users", JSON.stringify(users));
    alert("Registrierung erfolgreich! Jetzt anmelden.");
    toggleFormMode();
  }
}

function showWelcome(name) {
  authArea.style.display = "none";
  welcomeArea.style.display = "block";
  welcomeText.textContent = `Willkommen, ${name}!`;
  localStorage.setItem("currentUser", name);
}

function logoutUser() {
  welcomeArea.style.display = "none";
  authArea.style.display = "block";
  nameInput.value = "";
  passwordInput.value = "";
  localStorage.removeItem("currentUser");
}
submitBtn.addEventListener("click", handleSubmit);
document.getElementById("toggleMode").addEventListener("click", (e) => {
  e.preventDefault();
  toggleFormMode();
});
logout.addEventListener("click", logoutUser);