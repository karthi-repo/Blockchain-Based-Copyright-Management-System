const formOpenBtn = document.querySelector("#form-open"),
  formOpenBtn2 = document.querySelector("#GetStarted-open"),
  home = document.querySelector(".home"),
  formContainer = document.querySelector(".form_container"),
  formCloseBtn = document.querySelector(".form_close"),
  signupBtn = document.querySelector("#signup"),
  signupFrm = document.querySelector(".signup_form"),
  KeyGenBtn = document.querySelector("#genkey"),
  loginBtn = document.querySelector("#login"),
  pwShowHide = document.querySelectorAll(".pw_hide");
  
formOpenBtn.addEventListener("click", () => home.classList.add("show"));
formOpenBtn2.addEventListener("click", () => home.classList.add("show"));
formCloseBtn.addEventListener("click", () => home.classList.remove("show"));
pwShowHide.forEach((icon) => {
  icon.addEventListener("click", () => {
    let getPwInput = icon.parentElement.querySelector("input");
    if (getPwInput.type === "password") {
      getPwInput.type = "text";
      icon.classList.replace("uil-eye-slash", "uil-eye");
    } else {
      getPwInput.type = "password";
      icon.classList.replace("uil-eye", "uil-eye-slash");
    }
  });
});
signupBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.add("active");
});
loginBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.remove("active");
});

$('.showkeys').hide();
$("#logoncsign").hide();

function keygeneration() {
  KeyGenBtn.disabled = true;
  signupFrm.style.height = "500px";
  KeyGenBtn.addEventListener("mouseover", () => {
    KeyGenBtn.style.cursor = "default";
  });
  KeyGenBtn.style.color="#ceb0ff";

  async function generateKeyPair() {
    const keyPair = await window.crypto.subtle.generateKey(
      {
        name: 'RSA-OAEP',
        modulusLength: 2048,
        publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
        hash: 'SHA-256',
      },
      true,
      ['encrypt', 'decrypt']
    );
    const publicKey = await window.crypto.subtle.exportKey('spki', keyPair.publicKey);
    const privateKey = await window.crypto.subtle.exportKey('pkcs8', keyPair.privateKey);
    
    const publicKeyString = new TextDecoder().decode(publicKey).replace(/[^a-zA-Z0-9]/g, '');;
    const pubkeytextinp = document.querySelector("#pubkeytext");
    pubkeytextinp.value = publicKeyString;
    const privateKeyString = new TextDecoder().decode(privateKey).replace(/[^a-zA-Z0-9]/g, '');;
    const privatetextinp = document.querySelector("#privatetext");
    privatetextinp.value = privateKeyString;
    
    console.log('Private Key:', privateKey);
  }
  generateKeyPair();

  $(".login_signup").hide();
  $("#logoncsign").show();
  $('.showkeys').show();

}
KeyGenBtn.addEventListener("click", () => keygeneration());
