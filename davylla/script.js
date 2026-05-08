/* =====================================================================
   Site privado — 19 anos da Davylla
   Logica: caixa de presente -> 6 capitulos -> tela de assinatura
   Audio: trilha de fundo em loop (15%) durante toda a experiencia,
   com fade-out na tela final de assinatura.
   ===================================================================== */

(function () {
  'use strict';

  // ---------- ELEMENTOS GLOBAIS ----------
  const trilha = document.getElementById('trilha');
  const fadeOverlay = document.getElementById('fade-overlay');
  const abertura = document.getElementById('abertura');
  const caixa = document.getElementById('caixa-presente');
  const assinatura = document.getElementById('assinatura');
  const btnReiniciar = document.getElementById('reiniciar');
  const capitulos = Array.from(document.querySelectorAll('.capitulo'));

  // Volume da trilha de fundo: discreto e constante
  const VOLUME_FUNDO = 0.15;

  let trilhaIniciada = false;
  let capituloAtual = 0;    // 0 = abertura, 1..6 = capitulo, 7 = assinatura

  // ---------- INICIALIZA TRILHA ----------
  function iniciarTrilha() {
    if (trilhaIniciada) return;
    trilha.volume = VOLUME_FUNDO;
    const promessa = trilha.play();
    if (promessa !== undefined) {
      promessa.then(() => {
        trilhaIniciada = true;
      }).catch(() => {
        // autoplay bloqueado — vai tocar quando usuario interagir
      });
    }
  }

  // Tenta iniciar a trilha em qualquer primeiro toque/clique
  ['click', 'touchstart', 'keydown'].forEach((evt) => {
    document.addEventListener(evt, iniciarTrilha, { once: true, passive: true });
  });

  // ---------- ABERTURA DA CAIXA ----------
  function abrirCaixa() {
    if (caixa.classList.contains('abrindo')) return;
    iniciarTrilha();
    caixa.classList.add('abrindo');

    // Apos animacao da caixa (~3s), faz transicao pra capitulo 1
    setTimeout(() => {
      transicionar(() => {
        abertura.classList.remove('ativa');
        abertura.setAttribute('aria-hidden', 'true');
        ativarCapitulo(1);
      });
    }, 2800);
  }

  caixa.addEventListener('click', abrirCaixa);
  caixa.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter' || ev.key === ' ') {
      ev.preventDefault();
      abrirCaixa();
    }
  });

  // ---------- TRANSICAO COM FADE PRETO ----------
  function transicionar(callback) {
    fadeOverlay.classList.add('ativo');
    setTimeout(() => {
      try { callback(); } catch (e) { console.error(e); }
      // Pequeno respiro de silencio antes do proximo elemento aparecer
      setTimeout(() => {
        fadeOverlay.classList.remove('ativo');
      }, 600);
    }, 1500);
  }

  // ---------- ATIVAR CAPITULO ----------
  function ativarCapitulo(numero) {
    capituloAtual = numero;
    capitulos.forEach((cap) => {
      const n = parseInt(cap.dataset.capitulo, 10);
      if (n === numero) {
        cap.classList.add('ativa');
        cap.setAttribute('aria-hidden', 'false');
        // Rola pro topo do conteudo do capitulo (mobile)
        cap.scrollTop = 0;
      } else {
        cap.classList.remove('ativa');
        cap.setAttribute('aria-hidden', 'true');
      }
    });
  }

  // ---------- BOTAO PROXIMO ----------
  document.querySelectorAll('.btn-proximo').forEach((btn) => {
    btn.addEventListener('click', () => {
      const proximo = btn.dataset.proximo;
      if (proximo === 'final') {
        transicionar(() => {
          capitulos.forEach((c) => {
            c.classList.remove('ativa');
            c.setAttribute('aria-hidden', 'true');
          });
          mostrarAssinatura();
        });
      } else {
        const n = parseInt(proximo, 10);
        transicionar(() => ativarCapitulo(n));
      }
    });
  });

  // ---------- MOSTRAR TELA DE ASSINATURA ----------
  function mostrarAssinatura() {
    capituloAtual = 7;
    assinatura.classList.add('ativa');
    assinatura.setAttribute('aria-hidden', 'false');
    // Pausa suave da trilha na tela final (fade out)
    fadeOutTrilha(2500);
  }

  function fadeOutTrilha(duracao) {
    if (!trilhaIniciada) return;
    const passos = 50;
    const intervalo = duracao / passos;
    const volumeInicial = trilha.volume;
    let i = 0;
    const id = setInterval(() => {
      i++;
      trilha.volume = Math.max(0, volumeInicial * (1 - i / passos));
      if (i >= passos) {
        clearInterval(id);
        trilha.pause();
      }
    }, intervalo);
  }

  function fadeInTrilha(duracao, alvo) {
    const passos = 50;
    const intervalo = duracao / passos;
    trilha.volume = 0;
    if (trilha.paused) {
      try { trilha.play(); } catch (e) {}
    }
    let i = 0;
    const id = setInterval(() => {
      i++;
      trilha.volume = Math.min(alvo, alvo * (i / passos));
      if (i >= passos) clearInterval(id);
    }, intervalo);
  }

  // ---------- REINICIAR (botao na tela final "Ouvir desde o inicio") ----------
  btnReiniciar.addEventListener('click', () => {
    transicionar(() => {
      assinatura.classList.remove('ativa');
      assinatura.setAttribute('aria-hidden', 'true');
      capitulos.forEach((c) => {
        c.classList.remove('ativa');
        c.setAttribute('aria-hidden', 'true');
      });
      // Volta pra abertura
      capituloAtual = 0;
      abertura.classList.add('ativa');
      abertura.setAttribute('aria-hidden', 'false');
      caixa.classList.remove('abrindo');
      // Re-fade da trilha
      fadeInTrilha(2000, VOLUME_FUNDO);
    });
  });

  // ---------- TECLADO: setas ----------
  document.addEventListener('keydown', (ev) => {
    const ativo = document.querySelector('.capitulo.ativa');
    if (!ativo) return;
    const numero = parseInt(ativo.dataset.capitulo, 10);

    if (ev.key === 'ArrowRight') {
      const btn = ativo.querySelector('.btn-proximo');
      if (btn) btn.click();
    } else if (ev.key === 'ArrowLeft' && numero > 1) {
      transicionar(() => ativarCapitulo(numero - 1));
    }
  });

})();
