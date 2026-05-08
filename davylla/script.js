/* =====================================================================
   Site privado — 19 anos da Davylla
   Logica: caixa de presente -> 6 capitulos -> tela de assinatura
   Audio: trilha de fundo (loop, 15%) + narracao por capitulo (sob demanda)
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

  // Volume de fundo: discreto, conforme briefing
  const VOLUME_FUNDO = 0.15;
  const VOLUME_FUNDO_DURANTE_NARRACAO = 0.06;

  let trilhaIniciada = false;
  let narracaoAtiva = null; // referencia ao <audio> de narracao tocando

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
    pararNarracao();
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

  // ---------- CONTROLE DE NARRACAO ----------
  function pararNarracao() {
    if (narracaoAtiva) {
      narracaoAtiva.pause();
      narracaoAtiva.currentTime = 0;
      narracaoAtiva = null;
    }
    document.querySelectorAll('.btn-narracao').forEach((btn) => {
      const play = btn.querySelector('.icone-play');
      const pause = btn.querySelector('.icone-pause');
      const label = btn.querySelector('.btn-narracao-label');
      if (play) play.hidden = false;
      if (pause) pause.hidden = true;
      if (label) label.textContent = 'Ouvir narracao';
    });
    // Restaura volume da trilha
    if (trilhaIniciada && !trilha.paused) {
      trilha.volume = VOLUME_FUNDO;
    }
  }

  document.querySelectorAll('.btn-narracao').forEach((btn) => {
    const cap = btn.dataset.cap;
    const audio = document.getElementById('narracao-' + cap);
    const play = btn.querySelector('.icone-play');
    const pause = btn.querySelector('.icone-pause');
    const label = btn.querySelector('.btn-narracao-label');

    btn.addEventListener('click', () => {
      iniciarTrilha();

      // Se ja esta tocando essa narracao, pausa
      if (narracaoAtiva === audio && !audio.paused) {
        audio.pause();
        if (play) play.hidden = false;
        if (pause) pause.hidden = true;
        if (label) label.textContent = 'Continuar narracao';
        if (trilhaIniciada) trilha.volume = VOLUME_FUNDO;
        return;
      }

      // Para qualquer outra narracao
      pararNarracao();

      // Toca essa
      narracaoAtiva = audio;
      if (trilhaIniciada) trilha.volume = VOLUME_FUNDO_DURANTE_NARRACAO;
      audio.play().then(() => {
        if (play) play.hidden = true;
        if (pause) pause.hidden = false;
        if (label) label.textContent = 'Pausar narracao';
      }).catch((err) => {
        console.warn('Nao foi possivel tocar narracao:', err);
      });

      audio.onended = () => {
        if (play) play.hidden = false;
        if (pause) pause.hidden = true;
        if (label) label.textContent = 'Ouvir novamente';
        if (trilhaIniciada) trilha.volume = VOLUME_FUNDO;
        narracaoAtiva = null;
      };
    });
  });

  // ---------- REINICIAR (botao na tela final) ----------
  btnReiniciar.addEventListener('click', () => {
    transicionar(() => {
      assinatura.classList.remove('ativa');
      assinatura.setAttribute('aria-hidden', 'true');
      capitulos.forEach((c) => {
        c.classList.remove('ativa');
        c.setAttribute('aria-hidden', 'true');
      });
      // Volta pra abertura
      abertura.classList.add('ativa');
      abertura.setAttribute('aria-hidden', 'false');
      caixa.classList.remove('abrindo');
      // Re-fade da trilha
      fadeInTrilha(2000, VOLUME_FUNDO);
    });
  });

  // ---------- TECLADO: setas e ESC ----------
  document.addEventListener('keydown', (ev) => {
    const ativo = document.querySelector('.capitulo.ativa');
    if (!ativo) return;
    const numero = parseInt(ativo.dataset.capitulo, 10);

    if (ev.key === 'ArrowRight') {
      const btn = ativo.querySelector('.btn-proximo');
      if (btn) btn.click();
    } else if (ev.key === 'ArrowLeft' && numero > 1) {
      transicionar(() => ativarCapitulo(numero - 1));
    } else if (ev.key === 'Escape') {
      pararNarracao();
    }
  });

})();
