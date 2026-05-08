/* =====================================================================
   Site privado — 19 anos da Davylla
   Logica: caixa de presente -> 6 capitulos -> tela de assinatura
   Audio: trilha de fundo (loop, 15%) + narracao por capitulo (autoplay
   no momento que o capitulo abre, sob demanda do usuario via clique).
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
    pararNarracao();
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
    // Inicia narracao automaticamente assim que o capitulo entra em cena
    startNarrationFor(numero);
  }

  // ---------- BOTAO PROXIMO ----------
  document.querySelectorAll('.btn-proximo').forEach((btn) => {
    btn.addEventListener('click', () => {
      const proximo = btn.dataset.proximo;
      // Pausa/reseta narracao do cap atual antes de transicionar
      pararNarracao();
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

  // ---------- HELPERS DE BOTAO DE NARRACAO ----------
  function setBtnNarracaoEstado(numero, estado) {
    // estado: 'tocando' | 'pausado' | 'terminado' | 'reset'
    const btn = document.querySelector('.btn-narracao[data-cap="' + numero + '"]');
    if (!btn) return;
    const play = btn.querySelector('.icone-play');
    const pause = btn.querySelector('.icone-pause');
    const label = btn.querySelector('.btn-narracao-label');
    if (estado === 'tocando') {
      if (play) play.hidden = true;
      if (pause) pause.hidden = false;
      if (label) label.textContent = 'Pausar narracao';
    } else if (estado === 'pausado') {
      if (play) play.hidden = false;
      if (pause) pause.hidden = true;
      if (label) label.textContent = 'Continuar narracao';
    } else if (estado === 'terminado') {
      if (play) play.hidden = false;
      if (pause) pause.hidden = true;
      if (label) label.textContent = 'Ouvir novamente';
    } else {
      if (play) play.hidden = false;
      if (pause) pause.hidden = true;
      if (label) label.textContent = 'Ouvir narracao';
    }
  }

  function resetTodosBotoesNarracao() {
    document.querySelectorAll('.btn-narracao').forEach((btn) => {
      const play = btn.querySelector('.icone-play');
      const pause = btn.querySelector('.icone-pause');
      const label = btn.querySelector('.btn-narracao-label');
      if (play) play.hidden = false;
      if (pause) pause.hidden = true;
      if (label) label.textContent = 'Ouvir narracao';
    });
  }

  // ---------- CONTROLE DE NARRACAO ----------
  function pararNarracao() {
    if (narracaoAtiva) {
      try { narracaoAtiva.pause(); } catch (e) {}
      try { narracaoAtiva.currentTime = 0; } catch (e) {}
      narracaoAtiva = null;
    }
    resetTodosBotoesNarracao();
    // Restaura volume da trilha
    if (trilhaIniciada && !trilha.paused) {
      trilha.volume = VOLUME_FUNDO;
    }
  }

  // Inicia (ou tenta iniciar) a narracao do capitulo N automaticamente
  function startNarrationFor(numero) {
    const audio = document.getElementById('narracao-' + numero);
    if (!audio) return;

    // Garante que outras narracoes pararam
    if (narracaoAtiva && narracaoAtiva !== audio) {
      try { narracaoAtiva.pause(); } catch (e) {}
      try { narracaoAtiva.currentTime = 0; } catch (e) {}
    }
    narracaoAtiva = audio;

    // Reseta tempo (sempre comeca do inicio quando o capitulo abre)
    try { audio.currentTime = 0; } catch (e) {}

    // Baixa volume da trilha enquanto narracao toca
    if (trilhaIniciada) trilha.volume = VOLUME_FUNDO_DURANTE_NARRACAO;

    const promessa = audio.play();
    if (promessa !== undefined) {
      promessa.then(() => {
        setBtnNarracaoEstado(numero, 'tocando');
      }).catch((err) => {
        // Autoplay bloqueado — restaura UI pra usuario clicar manualmente
        console.warn('Autoplay narracao bloqueado, usuario precisa clicar:', err);
        if (trilhaIniciada) trilha.volume = VOLUME_FUNDO;
        setBtnNarracaoEstado(numero, 'reset');
      });
    } else {
      setBtnNarracaoEstado(numero, 'tocando');
    }

    // Quando narracao termina sozinha: NAO avanca, fica esperando usuario
    audio.onended = () => {
      if (trilhaIniciada) trilha.volume = VOLUME_FUNDO;
      setBtnNarracaoEstado(numero, 'terminado');
      narracaoAtiva = null;
    };
  }

  // Pausa a narracao do capitulo N (sem resetar tempo — permite continuar)
  function pauseNarrationFor(numero) {
    const audio = document.getElementById('narracao-' + numero);
    if (!audio) return;
    try { audio.pause(); } catch (e) {}
    if (trilhaIniciada) trilha.volume = VOLUME_FUNDO;
    setBtnNarracaoEstado(numero, 'pausado');
  }

  // ---------- BOTAO "OUVIR NARRACAO" (toggle Pausar / Continuar / Ouvir de novo) ----------
  document.querySelectorAll('.btn-narracao').forEach((btn) => {
    const cap = parseInt(btn.dataset.cap, 10);
    btn.addEventListener('click', () => {
      iniciarTrilha();
      const audio = document.getElementById('narracao-' + cap);
      if (!audio) return;

      // Caso 1: esta tocando agora -> pausa
      if (narracaoAtiva === audio && !audio.paused) {
        pauseNarrationFor(cap);
        return;
      }

      // Caso 2: esta pausada no meio (audio.currentTime > 0 e nao terminou) -> retoma
      if (narracaoAtiva === audio && audio.paused && audio.currentTime > 0 && !audio.ended) {
        if (trilhaIniciada) trilha.volume = VOLUME_FUNDO_DURANTE_NARRACAO;
        const p = audio.play();
        if (p !== undefined) {
          p.then(() => setBtnNarracaoEstado(cap, 'tocando'))
           .catch(() => setBtnNarracaoEstado(cap, 'pausado'));
        } else {
          setBtnNarracaoEstado(cap, 'tocando');
        }
        return;
      }

      // Caso 3: terminou ou esta zerada -> toca do inicio
      // (cobre tambem o caso de autoplay ter sido bloqueado)
      pararNarracao();
      startNarrationFor(cap);
    });
  });

  // ---------- REINICIAR (botao na tela final "Ouvir desde o inicio") ----------
  btnReiniciar.addEventListener('click', () => {
    pararNarracao();
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

  // ---------- TECLADO: setas e ESC ----------
  document.addEventListener('keydown', (ev) => {
    const ativo = document.querySelector('.capitulo.ativa');
    if (!ativo) return;
    const numero = parseInt(ativo.dataset.capitulo, 10);

    if (ev.key === 'ArrowRight') {
      const btn = ativo.querySelector('.btn-proximo');
      if (btn) btn.click();
    } else if (ev.key === 'ArrowLeft' && numero > 1) {
      pararNarracao();
      transicionar(() => ativarCapitulo(numero - 1));
    } else if (ev.key === 'Escape') {
      pararNarracao();
    }
  });

})();
