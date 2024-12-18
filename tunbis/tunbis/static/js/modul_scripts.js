document.addEventListener("DOMContentLoaded", function(event) {

    const showNavbar = (toggleId, navId, bodyId, headerId) => {
        const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            headerpd = document.getElementById(headerId);

        // Navbar başlangıçta açık
        nav.classList.add('show');
        bodypd.classList.add('body-pd');
        headerpd.classList.add('body-pd');

        // Tüm öğelerin mevcut olduğundan emin ol
        if (toggle && nav && bodypd && headerpd) {
            toggle.addEventListener('click', () => {
                // Navbar'ı kapatıp aç
                nav.classList.toggle('show');

                // İkon değişikliği
                toggle.classList.toggle('bx-x');

                // Gövde ve başlığa padding ekleyip çıkar
                bodypd.classList.toggle('body-pd');
                headerpd.classList.toggle('body-pd');
            });
        }
    }

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header');

    /*===== Linklerin Aktif Durumu =====*/
    const linkColor = document.querySelectorAll('.nav_link');

    function colorLink() {
        if (linkColor) {
            linkColor.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        }
    }
    linkColor.forEach(l => l.addEventListener('click', colorLink));
});