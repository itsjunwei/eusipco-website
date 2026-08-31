#!/usr/bin/env python3
"""Assemble content/references.json from the tutorial's four reference lists.

Phase 1 extraction. Structured fields are the source of truth; a formatted IEEE
string is generated from them so the site renders one consistent style.

INTEGRITY RULE: only DOIs / arXiv ids / URLs that appear in the source reference
lists are recorded here. Where the source gave no identifier, the field is left
null for Phase 2 verification to fill — nothing is invented.

Every entry starts verified=False; Phase 2 confirms authors/venue/pages/DOI.

Provenance keys:
  jw-list     source_materials/reference_lists/Tutorial-JW-IEEE-References.md
  joseph-doc  source_materials/reference_lists/Joseph_Section3_References.docx
  anc-authors / anc-others  Selected Publications on AI-ANC.pdf
  asi-authors / asi-others  Selected Publications on ASI.pdf

Section ids map to the tutorial outline (see outline.json):
  1 Spatial Perception (J.-W. Yeow)       2 Contextual Understanding (E.-L. Tan)
  3 Active Noise Control (W.-S. Gan)       4 Soundscape Augmentation (W.-S. Gan)
  5 Intelligent Sound Management (W.-S. Gan)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "references.json"


def ieee(r):
    s = f'{r["authors"]}, "{r["title"]},"'
    tail = f' *{r["venue"]}*'
    if r.get("info"):
        tail += f', {r["info"]}'
    if r.get("year"):
        tail += f', {r["year"]}'
    s += tail + "."
    if r.get("doi"):
        s += f' doi: {r["doi"]}.'
    elif r.get("arxiv"):
        s += f' arXiv:{r["arxiv"]}.'
    return s


def link(r):
    if r.get("doi"):
        return f'https://doi.org/{r["doi"]}'
    if r.get("arxiv"):
        return f'https://arxiv.org/abs/{r["arxiv"]}'
    return r.get("url")


ALL = []
SEEN_TITLE = {}   # normalized title -> id, for de-duplication


def register(items, section, provenance, prefix):
    for i, r in enumerate(items, 1):
        r = dict(r)
        sec = r.pop("sec", section)   # per-item section overrides the batch default
        key = r["title"].lower().strip()
        if key in SEEN_TITLE:
            # cross-list duplicate: attach this section to the existing entry
            existing = SEEN_TITLE[key]
            if sec not in existing["section"]:
                existing["section"].append(sec)
            existing["provenance"].append(provenance)
            continue
        r["id"] = f"{prefix}{i:02d}"
        r["section"] = [sec]
        r["provenance"] = [provenance]
        # Default verification. Sections 3–5 carry DOIs/arXiv ids from the presenters'
        # own curated publication lists ("source-doi"): resolvable, treated as verified,
        # but not independently re-checked this phase. Sections 1–2 are overridden by
        # VERIFY below with per-entry web-search results.
        r.setdefault("doi", None)
        r.setdefault("arxiv", None)
        r["verification"] = "source-doi"
        r["verified"] = True
        ALL.append(r)
        SEEN_TITLE[key] = r


# Phase 2 web-verification results for sections 1 & 2 (searched IEEE Xplore / arXiv /
# publisher pages, 2026-08-26). Each entry: identifiers found + verification status.
#   web        -> title/venue/year corroborated by an independent source this phase
#   unresolved -> no DOI/arXiv/stable link found; batched for the user
VERIFY = {
    "s1-01": {"url": "https://ieeexplore.ieee.org/document/9386249", "verification": "web"},
    "s1-02": {"verification": "web"},
    "s1-03": {"verification": "web"},
    "s1-04": {"verification": "web"},
    "s1-05": {"arxiv": "2111.08192", "verification": "web"},
    "s1-06": {"arxiv": "1807.00129", "verification": "web"},
    "s1-07": {"verification": "web"},
    "s1-08": {"arxiv": "2312.12821", "verification": "web"},
    "s1-09": {"arxiv": "2010.13092", "verification": "web"},
    "s1-10": {"verification": "web"},
    "s1-11": {"arxiv": "2110.07124", "verification": "web"},
    "s1-12": {"arxiv": "2403.11827", "verification": "web"},
    "s1-13": {"verification": "web"},
    "s1-14": {"doi": "10.1109/JSEN.2025.3583033", "verification": "web"},
    "s1-15": {"verification": "web"},
    "s1-16": {"verification": "web"},
    "s1-17": {"arxiv": "2401.12238", "verification": "web"},
    "s1-18": {"arxiv": "2509.15599", "verification": "web"},
    "s1-19": {"verification": "web"},
    "s1-20": {"arxiv": "2309.15938", "verification": "web"},
    "s1-21": {"arxiv": "2312.06907", "verification": "web"},
    "s1-22": {"doi": "10.1109/ICASSP49660.2025.10890626", "verification": "web"},
    "s1-23": {"arxiv": "2011.01819", "verification": "web"},
    "s1-24": {"arxiv": "2206.00970", "verification": "web"},
    "s1-25": {"arxiv": "2410.22803", "verification": "web"},
    "s1-32": {"verification": "web"},
    "s1-33": {"arxiv": "2406.16058", "verification": "web"},
    "s1-34": {"arxiv": "2402.01591", "verification": "web"},
    # Contextual Understanding: URL-only audit, 2026-08-31.
    "s2-01": {"url": "https://www.akustinenseura.fi/wp-content/uploads/2013/08/Heittola.pdf"},
    "s2-02": {"url": "https://doi.org/10.1186/1687-4722-2013-1"},
    "s2-03": {"url": "https://doi.org/10.1007/s00530-014-0424-7"},
    "s2-04": {"url": "https://doi.org/10.21437/Interspeech.2019-2169"},
    "s2-05": {"url": "https://doi.org/10.1109/WASPAA.2019.8937196"},
    "s2-06": {"url": "https://doi.org/10.1587/transinf.2020EDP7036"},
    "s2-07": {"url": "https://doi.org/10.1109/ICASSP40776.2020.9053912"},
    "s2-08": {"url": "https://doi.org/10.1109/IWAENC53105.2022.9914800"},
    "s2-09": {"url": "https://doi.org/10.1109/ICASSP40776.2020.9053702"},
    "s2-10": {"url": "https://www.apsipa.org/proceedings/2021/pdfs/0001156.pdf"},
    "s2-11": {"url": "https://doi.org/10.1016/j.apacoust.2024.110066"},
    "s2-12": {"url": "https://aes.org/publications/elibrary-page/?id=22938"},
    "s2-13": {"url": "https://arxiv.org/abs/2509.09931"},
    "s2-14": {"url": "https://dcase.community/documents/challenge2025/technical_reports/DCASE2023_Karasin_54_t1.pdf"},
    # Sound bubbles: source list had only a Semantic Scholar link; Nature Electronics DOI confirmed.
    "s4b-05": {"doi": "10.1038/s41928-024-01276-z", "url": None, "verification": "web"},
}


# ---------------------------------------------------------------------------
# SECTION 1 — Spatial Perception (J.-W. Yeow), slides 11–54.  Source: jw-list.
# Source already IEEE-formatted; identifiers transcribed exactly as given.
# ---------------------------------------------------------------------------
S1 = [
 dict(authors="E.-L. Tan, F. A. Karnapi, L. J. Ng, K. Ooi, and W.-S. Gan",
      title="Extracting urban sound information for residential areas in smart cities using an end-to-end IoT system",
      venue="IEEE Internet of Things Journal", info="vol. 8, no. 18, pp. 14308–14321", year=2021, type="journal"),
 dict(authors="J.-W. Yeow, E.-L. Tan, S. Peksi, and W.-S. Gan",
      title="Environmental acoustic intelligence through sound event localization and detection: A review",
      venue="npj Acoustics", info="vol. 1, art. no. 31", year=2025, type="journal",
      doi="10.1038/s44384-025-00036-3"),
 dict(authors="T. N. T. Nguyen, K. N. Watcharasupat, N. K. Nguyen, D. L. Jones, and W.-S. Gan",
      title="SALSA: Spatial cue-augmented log-spectrogram features for polyphonic sound event localization and detection",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="vol. 30, pp. 1749–1762", year=2022,
      type="journal", doi="10.1109/TASLP.2022.3173054"),
 dict(authors="K. Shimada et al.",
      title="Stereo sound event localization and detection with onscreen/offscreen classification",
      venue="arXiv preprint", year=2025, type="preprint", arxiv="2507.12042"),
 dict(authors="T. N. T. Nguyen, D. L. Jones, K. N. Watcharasupat, H. Phan, and W.-S. Gan",
      title="SALSA-Lite: A fast and effective feature for polyphonic sound event localization and detection with microphone arrays",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 716–720", year=2022,
      type="conference", url="https://ieeexplore.ieee.org/document/9746132"),
 dict(authors="S. Adavanne, A. Politis, J. Nikunen, and T. Virtanen",
      title="Sound event localization and detection of overlapping sources using convolutional recurrent neural networks",
      venue="IEEE Journal of Selected Topics in Signal Processing", info="vol. 13, no. 1, pp. 34–48", year=2019,
      type="journal", url="https://ieeexplore.ieee.org/document/8567942"),
 dict(authors="Q. Wang, J. Du, H.-X. Wu, J. Pan, F. Ma, and C.-H. Lee",
      title="A four-stage data augmentation approach to ResNet-Conformer based acoustic modeling for sound event localization and detection",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="vol. 31, pp. 1251–1264", year=2023,
      type="journal", url="https://ieeexplore.ieee.org/document/10068271"),
 dict(authors="Y. Shul and J.-W. Choi",
      title="CST-Former: Transformer with channel-spectro-temporal attention for sound event localization and detection",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 8686–8690", year=2024,
      type="conference", url="https://ieeexplore.ieee.org/document/10447181"),
 dict(authors="Y. Cao, T. Iqbal, Q. Kong, F. An, W. Wang, and M. D. Plumbley",
      title="An improved event-independent network for polyphonic sound event localization and detection",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 885–889", year=2021,
      type="conference", url="https://ieeexplore.ieee.org/document/9413473"),
 dict(authors="K. Shimada, Y. Koyama, N. Takahashi, S. Takahashi, and Y. Mitsufuji",
      title="ACCDOA: Activity-coupled Cartesian direction of arrival representation for sound event localization and detection",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 915–919", year=2021,
      type="conference", arxiv="2010.15306"),
 dict(authors="K. Shimada, Y. Koyama, S. Takahashi, N. Takahashi, E. Tsunoo, and Y. Mitsufuji",
      title="Multi-ACCDOA: Localizing and detecting overlapping sounds from the same class with auxiliary duplicating permutation invariant training",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 316–320", year=2022,
      type="conference", url="https://ieeexplore.ieee.org/document/9746384"),
 dict(authors="D. A. Krause, A. Politis, and A. Mesaros",
      title="Sound event detection and localization with distance estimation",
      venue="Proc. 32nd European Signal Processing Conference (EUSIPCO)", info="pp. 286–290", year=2024,
      type="conference", url="https://ieeexplore.ieee.org/document/10715220"),
 dict(authors="D. Berghi and P. J. B. Jackson",
      title="Reverberation-based features for sound event localization and detection with distance estimation",
      venue="IEEE Signal Processing Letters", info="vol. 33, pp. 1841–1845", year=2026, type="journal", doi="10.1109/LSP.2026.3685150"),
 dict(authors="J.-W. Yeow, E.-L. Tan, J. Bai, S. Peksi, and W.-S. Gan",
      title="Enhancing 3D sound event localization and detection with distance estimation using reverberation and spatial coherence features",
      venue="IEEE Sensors Journal", info="vol. 25, no. 15, pp. 29221–29237", year=2025, type="journal"),
      # DOI/pages confirmed via OpenAlex (10.1109/JSEN.2025.3583033) in the 2026-08-26 correction pass
 dict(authors="A. Politis, A. Mesaros, S. Adavanne, T. Heittola, and T. Virtanen",
      title="Overview and evaluation of sound event localization and detection in DCASE 2019",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="vol. 29, pp. 684–698", year=2021,
      type="journal", doi="10.1109/TASLP.2020.3047233"),
 dict(authors="D. Diaz-Guerra et al.",
      title="Baseline models and evaluation of sound event localization and detection with distance estimation in DCASE2024 Challenge",
      venue="Proc. Detection and Classification of Acoustic Scenes and Events Workshop (DCASE)", info="Tokyo, Japan, pp. 41–45", year=2024,
      type="workshop",
      url="https://dcase.community/documents/workshop2024/proceedings/DCASE2024Workshop_Diaz-Guerra_53.pdf"),
 dict(authors="I. R. Roman, C. Ick, S. Ding, A. S. Roman, B. McFee, and J. P. Bello",
      title="Spatial Scaper: A library to simulate and augment soundscapes for sound event localization and detection in realistic rooms",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", year=2024, type="conference",
      url="https://ieeexplore.ieee.org/document/10446118"),
 dict(authors="J.-W. Yeow, E.-L. Tan, S. Peksi, and W.-S. Gan",
      title="MAGENTA: Magnitude and geometry-enhanced training approach for robust long-tailed sound event localization and detection",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="pp. 1–14", year=2026,
      type="journal", url="https://ieeexplore.ieee.org/document/11656345"),
 dict(authors="J. Hu, Y. Cao, M. Wu, F. Kang, F. Yang, W. Wang, M. D. Plumbley, and J. Yang",
      title="PSELDNets: Pre-trained neural networks on a large-scale synthetic dataset for sound event localization and detection",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="vol. 33, pp. 2845–2860", year=2025,
      type="journal", doi="10.1109/TASLPRO.2025.3587446"),
 dict(authors="X. Jiang, C. Han, Y. A. Li, and N. Mesgarani",
      title="Exploring self-supervised contrastive learning of spatial sound event representation",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 1281–1285", year=2024,
      type="conference", url="https://ieeexplore.ieee.org/document/10447391"),
 dict(authors="O. L. dos Santos, K. Rosero, B. Masiero, and R. de A. Lotufo",
      title="w2v-SELD: A sound event localization and detection framework for self-supervised spatial audio pre-training",
      venue="IEEE Access", info="vol. 12, pp. 181553–181569", year=2024, type="journal",
      url="https://ieeexplore.ieee.org/document/10772471"),
 dict(authors="Y. Nozaki, Y. Bando, and M. Onishi",
      title="Source-aware spatial self-supervision for sound event localization and detection",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 1–5", year=2025,
      type="conference", url="https://ieeexplore.ieee.org/document/10890626"),
 dict(authors="P. Morgado, Y. Li, and N. Vasconcelos",
      title="Learning representations from audio-visual spatial alignment",
      venue="Advances in Neural Information Processing Systems (NeurIPS)", info="vol. 33, pp. 4733–4744", year=2020,
      type="conference",
      url="https://proceedings.neurips.cc/paper/2020/hash/328e5d4c166bb340b314d457a208dc83-Abstract.html"),
 dict(authors="S. Wang, A. Politis, A. Mesaros, and T. Virtanen",
      title="Self-supervised learning of audio representations from audio-visual data using spatial alignment",
      venue="IEEE Journal of Selected Topics in Signal Processing", info="vol. 16, no. 6, pp. 1467–1479", year=2022,
      type="journal", url="https://ieeexplore.ieee.org/document/9790080"),
 dict(authors="Y. Fujita, Y. Bando, K. Imoto, M. Onishi, and K. Yoshii",
      title="DOA-aware audio-visual self-supervised learning for sound event localization and detection",
      venue="Proc. Asia-Pacific Signal Inf. Process. Assoc. Annu. Summit Conf. (APSIPA ASC)", info="pp. 2061–2067", year=2023,
      type="conference", url="https://ieeexplore.ieee.org/document/10317433"),
 dict(authors="S. Deshmukh et al.",
      title="Pengi: An audio language model for audio tasks",
      venue="Advances in Neural Information Processing Systems (NeurIPS)", info="vol. 36, pp. 18090–18108", year=2023,
      type="conference", arxiv="2305.11834"),
 dict(authors="Y. Gong, H. Luo, A. H. Liu, L. Karlinsky, and J. Glass",
      title="Listen, think, and understand",
      venue="Proc. 12th Int. Conf. Learning Representations (ICLR)", year=2024, type="conference", arxiv="2305.10790"),
 dict(authors="C. Tang, W. Yu, G. Sun, X. Chen, T. Tan, W. Li, L. Lu, Z. Ma, and C. Zhang",
      title="SALMONN: Towards generic hearing abilities for large language models",
      venue="Proc. 12th Int. Conf. Learning Representations (ICLR)", year=2024, type="conference", arxiv="2310.13289"),
 dict(authors="Y. Chu et al.",
      title="Qwen2-Audio technical report",
      venue="arXiv preprint", year=2024, type="preprint", arxiv="2407.10759"),
 dict(authors="Kimi Team et al.",
      title="Kimi-Audio technical report",
      venue="arXiv preprint", year=2025, type="preprint", arxiv="2504.18425"),
 dict(authors="A. Huang et al.",
      title="Step-Audio: Unified understanding and generation in intelligent speech interaction",
      venue="arXiv preprint", year=2025, type="preprint", arxiv="2502.11946"),
 dict(authors="K. Shimada et al.",
      title="Open-vocabulary sound event localization and detection with joint learning of CLAP embedding and activity-coupled Cartesian DOA vector",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", year=2025, type="journal",
      url="https://ieeexplore.ieee.org/document/11074724"),
 dict(authors="J. Zhao, X. Qian, Y. Xu, H. Liu, Y. Cao, D. Berghi, and W. Wang",
      title="Text-queried target sound event localization",
      venue="Proc. 32nd European Signal Processing Conference (EUSIPCO)", info="pp. 261–265", year=2024,
      type="conference", url="https://ieeexplore.ieee.org/document/10715199"),
 dict(authors="Z. Zheng, P. Peng, Z. Ma, X. Chen, E. Choi, and D. Harwath",
      title="BAT: Learning to reason about spatial sounds with large language models",
      venue="Proc. 41st Int. Conf. Machine Learning (ICML)", info="vol. 235, pp. 61454–61469", year=2024,
      type="conference", url="https://proceedings.mlr.press/v235/zheng24i.html"),
 dict(authors="S. Sakshi, V. Lokegaonkar, N. Zhang, R. Duraiswami, S. Ghosh, D. Manocha, and L. Lu",
      title="SPUR: A plug-and-play framework for integrating spatial audio understanding and reasoning into large audio-language models",
      venue="arXiv preprint", year=2025, type="preprint", arxiv="2511.06606"),
]
register(S1, "1", "jw-list", "s1-")

# ---------------------------------------------------------------------------
# SECTION 2 — Contextual Understanding (E.-L. Tan), slides 55–81.
# Source: joseph-doc (titled "Section 3" there — see PROGRESS numbering note).
# Source gave author/title/venue/year only; no identifiers are added.
# ---------------------------------------------------------------------------
S2 = [
 dict(authors="T. Heittola et al.",
      title="Sound event detection and context recognition",
      venue="Proceedings of Akustiikkapäivät", year=2011, type="conference"),
 dict(authors="T. Heittola et al.",
      title="Context-dependent sound event detection",
      venue="EURASIP Journal on Audio, Speech, and Music Processing", year=2013, type="journal"),
 dict(authors="T. Lu et al.",
      title="Context-based environmental audio event recognition for scene understanding",
      venue="Multimedia Systems", year=2015, type="journal"),
 dict(authors="H.L. Bear et al.",
      title="Towards joint sound scene and polyphonic sound event recognition",
      venue="Interspeech", year=2019, type="conference"),
 dict(authors="N. Tonami et al.",
      title="Joint analysis of acoustic events and scenes based on multitask learning",
      venue="IEEE WASPAA", year=2019, type="conference"),
 dict(authors="N. Tonami et al.",
      title="Joint analysis of sound events and acoustic scenes using multitask learning",
      venue="IEICE Transactions on Information and Systems", year=2021, type="journal"),
 dict(authors="K. Imoto et al.",
      title="Sound event detection by multitask learning of sound events and scenes with soft scene labels",
      venue="IEEE ICASSP", year=2020, type="conference"),
 dict(authors="S. Tsubaki et al.",
      title="Joint analysis of acoustic scenes and sound events with weakly labeled data",
      venue="IWAENC", year=2022, type="conference"),
 dict(authors="T. Komatsu et al.",
      title="Scene-dependent acoustic event detection with scene conditioning and fake-scene-conditioned loss",
      venue="IEEE ICASSP", year=2020, type="conference"),
 dict(authors="K. Nada et al.",
      title="Multitask learning of acoustic scenes and events using dynamic weight adaptation based on multi-focal loss",
      venue="APSIPA", year=2021, type="conference"),
 dict(authors="H. Zhang  et al.",
      title="An event-scene cooperative analysis network with dual-stream attention convolution module and soft parameter-sharing",
      venue="Applied Acoustics", year=2024, type="journal"),
 dict(authors="J.-W. Yeow, et al.",
      title="Enhancing situational awareness in wearable audio devices using a lightweight sound event localization and detection system",
      venue="AES International Conference on Headphone Technology", year=2025, type="conference"),
 dict(authors="E.-L. Tan, et al.",
      title="Acoustic scene classification using CNN-GRU Model without knowledge distillation",
      venue="arXiv preprint", year=2025, type="preprint"),
 dict(authors="D. Karasin et al.",
      title="Domain-specific external data pre-training and device-aware distillation for data-efficient acoustic scene classification",
      venue=",DCASe Task 1 Technical report", year=2025, type="report"),
]
register(S2, "2", "joseph-doc", "s2-")

# ---------------------------------------------------------------------------
# SECTION 3 — Active Noise Control (W.-S. Gan), slides 82–150.
# Source: anc-authors + anc-others (AI-ANC.pdf). DOIs present in source.
# ---------------------------------------------------------------------------
S3a = [
 dict(authors="X. Su, D. Shi, B. Wu, L. Ye, and W.-S. Gan",
      title="Co-forecasting of time-varying spatial-frequency map for selective fixed-filter multichannel ANC based on dynamic factor graph",
      venue="IEEE Transactions on Audio, Speech and Language Processing", info="vol. 33, pp. 2232–2243", year=2025,
      type="journal", doi="10.1109/TASLPRO.2025.3570939"),
 dict(authors="Z. Luo, H. Ma, B. Wang, Z. Yang, D. Shi, and W.-S. Gan",
      title="A stabilized hybrid active noise control algorithm of GFANC and FxNLMS with online clustering",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 14912–14916", year=2026,
      type="conference", doi="10.1109/ICASSP55912.2026.11460979"),
 dict(authors="Z. Luo, D. Shi, X. Su, and W.-S. Gan",
      title="Frequency-direction aware multichannel selective fixed-filter active noise control based on multi-task learning",
      venue="IEEE Transactions on Audio, Speech and Language Processing", info="vol. 33, pp. 3137–3147", year=2025,
      type="journal", doi="10.1109/TASLPRO.2025.3590289"),
 dict(authors="B. Wang, D. Shi, Z. Luo, X. Shen, J. Ji, and W.-S. Gan",
      title="Transferable selective virtual sensing active noise control technique based on metric learning",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 1–5", year=2025,
      type="conference", doi="10.1109/ICASSP49660.2025.10887958"),
 dict(authors="X. Su, D. Shi, Z. Zhu, W.-S. Gan, and L. Ye",
      title="Spatial-frequency-based selective fixed-filter algorithm for multichannel active noise control",
      venue="IEEE Signal Processing Letters", info="vol. 31, pp. 2635–2639", year=2024,
      type="journal", doi="10.1109/LSP.2024.3465889"),
 dict(authors="Z. Luo, D. Shi, X. Shen, and W.-S. Gan",
      title="Unsupervised learning based end-to-end delayless generative fixed-filter active noise control",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 441–445", year=2024,
      type="conference", doi="10.1109/ICASSP48485.2024.10448277"),
 dict(authors="Z. Luo, D. Shi, W.-S. Gan, and Q. Huang",
      title="Delayless generative fixed-filter active noise control based on deep learning and Bayesian filter",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="vol. 32, pp. 1048–1060", year=2024,
      type="journal", doi="10.1109/TASLP.2023.3337632"),
 dict(authors="Z. Luo, D. Shi, X. Shen, J. Ji, and W.-S. Gan",
      title="GFANC-Kalman: Generative fixed-filter active noise control with CNN-Kalman filtering",
      venue="IEEE Signal Processing Letters", info="vol. 31, pp. 276–280", year=2024,
      type="journal", doi="10.1109/LSP.2023.3334695"),
 dict(authors="Z. Luo, D. Shi, X. Shen, J. Ji, and W.-S. Gan",
      title="Deep generative fixed-filter active noise control",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 1–5", year=2023,
      type="conference", doi="10.1109/ICASSP49357.2023.10095205"),
 dict(authors="D. Shi, W.-S. Gan, B. Lam, Z. Luo, and X. Shen",
      title="Transferable latent of CNN-based selective fixed-filter active noise control",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="vol. 31, pp. 2910–2921", year=2023,
      type="journal", doi="10.1109/TASLP.2023.3261757"),
 dict(authors="Z. Luo, D. Shi, and W.-S. Gan",
      title="A hybrid SFANC-FxNLMS algorithm for active noise control based on deep learning",
      venue="IEEE Signal Processing Letters", info="vol. 29, pp. 1102–1106", year=2022,
      type="journal", doi="10.1109/LSP.2022.3169428"),
 dict(authors="D. Shi, W.-S. Gan, B. Lam, and S. Wen",
      title="Feedforward selective fixed-filter active noise control: Algorithm and implementation",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="vol. 28, pp. 1479–1492", year=2020,
      type="journal", doi="10.1109/TASLP.2020.2989582"),
 dict(authors="D. Y. Shi, B. Lam, and W.-S. Gan",
      title="A novel selective active noise control algorithm to overcome practical implementation issue",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 1130–1134", year=2018,
      type="conference", doi="10.1109/ICASSP.2018.8461458"),
 dict(authors="D. Shi, B. Lam, K. Ooi, X. Shen, and W.-S. Gan",
      title="Selective fixed-filter active noise control based on convolutional neural network",
      venue="Signal Processing", info="vol. 190, art. no. 108317", year=2022,
      type="journal", doi="10.1016/j.sigpro.2021.108317"),
 dict(authors="B. Wang, H. Li, D. Shi, J. Ji, Z. Yang, Z. Luo, and W.-S. Gan",
      title="Spatial-frequency cued generative fixed-filter active noise control based on deep learning in reverberant environments",
      venue="Signal Processing", info="vol. 247, art. no. 110682", year=2026,
      type="journal", doi="10.1016/j.sigpro.2026.110682"),
 dict(authors="Z. Luo, H. Ma, B. Wang, D. Shi, and W.-S. Gan",
      title="Reinforcement learning-based selective fixed-filter active noise control (RL-SFANC): From theory to real-time headphone implementation",
      venue="Signal Processing", info="vol. 248, art. no. 110695", year=2026,
      type="journal", doi="10.1016/j.sigpro.2026.110695"),
 dict(authors="Z. Luo, D. Shi, J. Ji, X. Shen, and W.-S. Gan",
      title="Real-time implementation and explainable AI analysis of delayless CNN-based selective fixed-filter active noise control",
      venue="Mechanical Systems and Signal Processing", info="vol. 214, art. no. 111364", year=2024,
      type="journal", doi="10.1016/j.ymssp.2024.111364"),
 dict(authors="Z. Luo, J. Ji, B. Wang, D. Shi, H. Ma, and W.-S. Gan",
      title="Deep learning-based generative fixed-filter active noise control: Transferability and implementation",
      venue="Mechanical Systems and Signal Processing", info="vol. 238, art. no. 113207", year=2025,
      type="journal", doi="10.1016/j.ymssp.2025.113207"),
 dict(authors="Z. Luo, H. Ma, D. Shi, and W.-S. Gan",
      title="GFANC-RL: Reinforcement learning-based generative fixed-filter active noise control",
      venue="Neural Networks", info="vol. 180, art. no. 106687", year=2024,
      type="journal", doi="10.1016/j.neunet.2024.106687"),
 dict(authors="Y. Hou, Q. Ren, H. Zhang, A. Mitchell, F. Aletta, J. Kang, and D. Botteldooren",
      title="AI-based soundscape analysis: Jointly identifying sound sources and predicting annoyance",
      venue="The Journal of the Acoustical Society of America", info="vol. 154, no. 5, pp. 3145–3157", year=2023,
      type="journal", doi="10.1121/10.0022408"),
]
register(S3a, "3", "anc-authors", "s3a-")

S3b = [
 dict(authors="D. Wu, X. Wu, and T. Qu",
      title="A hybrid deep-online learning based method for active noise control in wave domain",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 1301–1305", year=2024,
      type="conference", doi="10.1109/ICASSP48485.2024.10446791"),
 dict(authors="H. Zhang, A. Pandey, and D. L. Wang",
      title="Low-latency active noise control using attentive recurrent network",
      venue="IEEE/ACM Transactions on Audio, Speech, and Language Processing", info="vol. 31, pp. 1114–1123", year=2023,
      type="journal", doi="10.1109/TASLP.2023.3244528"),
 dict(authors="Fareedha, Vasundhara, A. Kar, and M. G. Christensen",
      title="Joint deep secondary path estimation and adaptive control for active noise cancellation",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 15177–15181", year=2026,
      type="conference", doi="10.1109/ICASSP55912.2026.11461474"),
 dict(authors="C. Cheng, Z. Liu, W. Chen, X. Li, W. Liao, and C. Lu",
      title="A multi-channel active noise control system using deep learning-based method to estimate secondary path and normalized-clustered control strategy for vehicle interior engine noise",
      venue="Applied Acoustics", info="vol. 228, art. no. 110263", year=2025,
      type="journal", doi="10.1016/j.apacoust.2024.110263"),
 dict(authors="J. Y. Oh, H. W. Jung, M. H. Lee, K. H. Lee, and Y. J. Kang",
      title="Enhancing active noise control of road noise using deep neural network to update secondary path estimate in real time",
      venue="Mechanical Systems and Signal Processing", info="vol. 206, art. no. 110940", year=2024,
      type="journal", doi="10.1016/j.ymssp.2023.110940"),
 dict(authors="J. Y. Oh, J. Y. Kim, C. S. Oh, J. H. Doe, and Y. J. Kang",
      title="Head-tracking active road noise control by real-time path adaptation using neural networks",
      venue="Mechanical Systems and Signal Processing", info="vol. 250, art. no. 114106", year=2026,
      type="journal", doi="10.1016/j.ymssp.2026.114106"),
 dict(authors="L. Bai, S. Lian, M. Li, Y. He, L. Rao, X. Zeng, R. Sun, K. Chen, and J. Lu",
      title="WaveNet-Volterra neural network for active noise control: A fully causal approach",
      venue="Mechanical Systems and Signal Processing", info="vol. 241, art. no. 113486", year=2025,
      type="journal", doi="10.1016/j.ymssp.2025.113486"),
 dict(authors="H. Zhang and D. Wang",
      title="Deep ANC: A deep learning approach to active noise control",
      venue="Neural Networks", info="vol. 141, pp. 1–10", year=2021,
      type="journal", doi="10.1016/j.neunet.2021.03.037"),
 dict(authors="H. Zhang and D. Wang",
      title="Deep MCANC: A deep learning approach to multi-channel active noise control",
      venue="Neural Networks", info="vol. 158, pp. 318–327", year=2023,
      type="journal", doi="10.1016/j.neunet.2022.11.029"),
 dict(authors="Y.-J. Cha, A. Mostafavi, and S. S. Benipal",
      title="DNoiseNet: Deep learning-based feedback active noise control in various noisy environments",
      venue="Engineering Applications of Artificial Intelligence", info="vol. 121, art. no. 105971", year=2023,
      type="journal", doi="10.1016/j.engappai.2023.105971"),
 dict(authors="A. Aboutiman, K. S. A. Maamoun, H. R. Karimi, and F. Ripamonti",
      title="Hybrid deep learning-based active noise control for encapsulated structures with openings",
      venue="Expert Systems with Applications", info="vol. 309, art. no. 131247", year=2026,
      type="journal", doi="10.1016/j.eswa.2026.131247"),
 dict(authors="L. Yin, Z. Zhang, M. Wu, S. Zhou, J. Guo, J. Yang, and J. Zhang",
      title="Selective fixed-filter active noise control based on frequency response matching in headphones",
      venue="Applied Acoustics", info="vol. 211, art. no. 109505", year=2023,
      type="journal", doi="10.1016/j.apacoust.2023.109505"),
 dict(authors="A. Aboutiman, Z. Rachman, T. Oberman, F. Aletta, J. Kang, H. R. Karimi, and F. Ripamonti",
      title="Subjective perception analysis of active noise control algorithms in an encapsulated structure: An experimental study",
      venue="Applied Acoustics", info="vol. 239, art. no. 110823", year=2025,
      type="journal", doi="10.1016/j.apacoust.2025.110823"),
 dict(authors="L. Yin, Z. Zhang, M. Wu, Z. Wang, C. Ma, S. Zhou, and J. Yang",
      title="Adaptive parallel filter method for active cancellation of road noise inside vehicles",
      venue="Mechanical Systems and Signal Processing", info="vol. 193, art. no. 110274", year=2023,
      type="journal", doi="10.1016/j.ymssp.2023.110274"),
]
register(S3b, "3", "anc-others", "s3b-")

# ---------------------------------------------------------------------------
# SECTIONS 4 & 5 — Active Sound Intervention (W.-S. Gan).
# Source: asi-authors + asi-others (ASI.pdf). Split by topic:
#   4 Soundscape Augmentation (slides 151–160)
#   5 Intelligent Sound Management / hearables (slides 161–183)
# DOIs present in source except where noted.
# ---------------------------------------------------------------------------
S4a = [  # asi-authors -> soundscape (section 4) unless noted
 dict(sec="4", authors="K. Ooi, Z.-T. Ong, K. N. Watcharasupat, B. Lam, J. Y. Hong, and W.-S. Gan",
      title="ARAUS: A large-scale dataset and baseline models of affective responses to augmented urban soundscapes",
      venue="IEEE Transactions on Affective Computing", info="vol. 15, no. 1, pp. 105–120", year=2024,
      type="journal", doi="10.1109/TAFFC.2023.3247914"),
 dict(sec="4", authors="K. Ooi, K. N. Watcharasupat, B. Lam, Z.-T. Ong, and W.-S. Gan",
      title="Autonomous soundscape augmentation with multimodal fusion of visual and participant-linked inputs",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 1–5", year=2023,
      type="conference", doi="10.1109/ICASSP49357.2023.10094866"),
 dict(sec="4", authors="K. N. Watcharasupat, K. Ooi, B. Lam, T. Wong, Z.-T. Ong, and W.-S. Gan",
      title="Autonomous in-situ soundscape augmentation via joint selection of masker and gain",
      venue="IEEE Signal Processing Letters", info="vol. 29, pp. 1749–1753", year=2022,
      type="journal", doi="10.1109/LSP.2022.3194419"),
 dict(sec="4", authors="K. Ooi, K. N. Watcharasupat, B. Lam, Z.-T. Ong, and W.-S. Gan",
      title="Probably pleasant? A neural-probabilistic approach to automatic masker selection for urban soundscape augmentation",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 8887–8891", year=2022,
      type="conference", doi="10.1109/ICASSP43922.2022.9746897"),
 dict(sec="4", authors="J. Y. Hong, B. Lam, Z.-T. Ong, K. Ooi, W.-S. Gan, J. Kang, S. Yeong, I. Lee, and S.-T. Tan",
      title="The effects of spatial separations between water sound and traffic noise sources on soundscape assessment",
      venue="Building and Environment", info="vol. 167, art. no. 106423", year=2020,
      type="journal", doi="10.1016/j.buildenv.2019.106423"),
 dict(sec="4", authors="B. Lam, Z.-T. Ong, K. Ooi, W.-H. Ong, T. Wong, K. N. Watcharasupat, V. Boey, I. Lee, J. Y. Hong, J. Kang, K. F. A. Lee, G. Christopoulos, and W.-S. Gan",
      title="Automating urban soundscape enhancements with AI: In-situ assessment of quality and restorativeness in traffic-exposed residential areas",
      venue="Building and Environment", info="vol. 266, art. no. 112106", year=2024,
      type="journal", doi="10.1016/j.buildenv.2024.112106"),
 dict(sec="4", authors="J. Y. Hong, Z.-T. Ong, B. Lam, K. Ooi, W.-S. Gan, J. Kang, J. Feng, and S.-T. Tan",
      title="Effects of adding natural sounds to urban noises on the perceived loudness of noise and soundscape quality",
      venue="Science of The Total Environment", info="vol. 711, art. no. 134571", year=2020,
      type="journal", doi="10.1016/j.scitotenv.2019.134571"),
 dict(sec="4", authors="J. Y. Hong, B. Lam, Z.-T. Ong, K. Ooi, W.-S. Gan, J. Kang, S. Yeong, I. Lee, and S.-T. Tan",
      title="A mixed-reality approach to soundscape assessment of outdoor urban environments augmented with natural sounds",
      venue="Building and Environment", info="vol. 194, art. no. 107688", year=2021,
      type="journal", doi="10.1016/j.buildenv.2021.107688"),
 dict(sec="4", authors="B. Lam, E. M. P. Fan, K. Ooi, Z.-T. Ong, J. Y. Hong, W.-S. Gan, and S. Y. Ang",
      title="Assessing the perceived indoor acoustic environment quality across building occupants in a tertiary-care public hospital in Singapore",
      venue="Building and Environment", info="vol. 222, art. no. 109403", year=2022,
      type="journal", doi="10.1016/j.buildenv.2022.109403"),
 dict(sec="4", authors="J. Y. Hong, B. Lam, Z.-T. Ong, K. Ooi, W.-S. Gan, and S. Lee",
      title="A multidimensional assessment of construction machinery noises based on perceptual attributes and psychoacoustic parameters",
      venue="Automation in Construction", info="vol. 140, art. no. 104295", year=2022,
      type="journal", doi="10.1016/j.autcon.2022.104295"),
 dict(sec="4", authors="J. Y. Hong, B. Lam, Z.-T. Ong, K. Ooi, W.-S. Gan, J. Kang, S. Yeong, I. Lee, and S.-T. Tan",
      title="Effects of contexts in urban residential areas on the pleasantness and appropriateness of natural sounds",
      venue="Sustainable Cities and Society", info="vol. 63, art. no. 102475", year=2020,
      type="journal", doi="10.1016/j.scs.2020.102475"),
 dict(sec="4", authors="B. Lam, K. C. Q. Lim, K. Ooi, Z.-T. Ong, D. Shi, and W.-S. Gan",
      title="Anti-noise window: Subjective perception of active noise reduction and effect of informational masking",
      venue="Sustainable Cities and Society", info="vol. 97, art. no. 104763", year=2023,
      type="journal", doi="10.1016/j.scs.2023.104763"),
 dict(sec="5", authors="R. Gupta, J. He, R. Ranjan, W.-S. Gan, F. Klein, C. Schneiderwind, A. Neidhardt, K. Brandenburg, and V. Välimäki",
      title="Augmented/mixed reality audio for hearables: Sensing, control, and rendering",
      venue="IEEE Signal Processing Magazine", info="vol. 39, no. 3, pp. 63–89", year=2022,
      type="journal", doi="10.1109/MSP.2021.3110108"),
]
register(S4a, None, "asi-authors", "s4a-")

S4b = [  # asi-others
 dict(sec="4", authors="Y. Hou, Q. Ren, H. Zhang, A. Mitchell, F. Aletta, J. Kang, and D. Botteldooren",
      title="AI-based soundscape analysis: Jointly identifying sound sources and predicting annoyance",
      venue="The Journal of the Acoustical Society of America", info="vol. 154, no. 5, pp. 3145–3157", year=2023,
      type="journal", doi="10.1121/10.0022408"),
 dict(sec="4", authors="Y. Hou, Q. Ren, A. Mitchell, W. Wang, J. Kang, T. Belpaeme, and D. Botteldooren",
      title="Soundscape captioning using sound affective quality network and large language model",
      venue="IEEE Transactions on Multimedia", info="vol. 28, pp. 2186–2200", year=2026,
      type="journal", doi="10.1109/TMM.2026.3651023"),
 dict(sec="4", authors="Y. Hou, S. Song, C. Luo, A. Mitchell, Q. Ren, W. Xie, J. Kang, W. Wang, and D. Botteldooren",
      title="Joint prediction of audio event and annoyance rating in an urban soundscape by hierarchical graph representation learning",
      venue="arXiv preprint", year=2023, type="preprint", arxiv="2308.11980"),
 dict(sec="4", authors="Y. Hou, Q. Ren, S. Song, Y. Song, W. Wang, and D. Botteldooren",
      title="Multi-level graph learning for audio event classification and human-perceived annoyance rating prediction",
      venue="Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP)", info="pp. 716–720", year=2024,
      type="conference", doi="10.1109/ICASSP48485.2024.10446633"),
 dict(sec="5", authors="T. Chen, M. Itani, S. E. Eskimez, T. Yoshioka, and S. Gollakota",
      title="Hearable devices with sound bubbles",
      venue="Nature Electronics", info="vol. 7, pp. 1047–1058", year=2024, type="journal",
      url="https://api.semanticscholar.org/CorpusID:274068539"),
 dict(sec="5", authors="B. Veluri, M. Itani, J. Chan, T. Yoshioka, and S. Gollakota",
      title="Semantic hearing: Programming acoustic scenes with binaural hearables",
      venue="Proc. 36th Annual ACM Symp. User Interface Software and Technology (UIST)", info="pp. 1–15", year=2023,
      type="conference", doi="10.1145/3586183.3606779"),
 dict(sec="5", authors="K. Yuan, F. Y. Liu, T. Xiao, Y. Song, C. Shen, S. Bhutani, J. Chan, and S. Kumar",
      title="Active noise cancellation on open-ear smart glasses",
      venue="arXiv preprint", year=2026, type="preprint", arxiv="2604.05519"),
 dict(sec="4", authors="Y. Liang, A. Mitchell, J. Kang, and F. Aletta",
      title="A review of soundscape datasets: Challenges and prospects for multimodal research",
      venue="IEEE Transactions on Affective Computing", info="vol. 17, no. 2, pp. 1505–1520", year=2026,
      type="journal", doi="10.1109/TAFFC.2026.3659084"),
]
register(S4b, None, "asi-others", "s4b-")

# ---------------------------------------------------------------------------
# Phase 2 corrections
# ---------------------------------------------------------------------------
for r in ALL:
    if r["id"].startswith("s2-"):
        r["verification"] = "unresolved"
    if r["id"] in VERIFY:
        upd = VERIFY[r["id"]]
        for k, v in upd.items():
            r[k] = v
    r["verified"] = r["verification"] != "unresolved"
    r["url"] = link(r)
    r["ieee"] = ieee(r)

# ---------------------------------------------------------------------------
# Finalize
# ---------------------------------------------------------------------------
by_section = {}
for r in ALL:
    for s in r["section"]:
        by_section[s] = by_section.get(s, 0) + 1

n_web = sum(1 for r in ALL if r["verification"] == "web")
n_src = sum(1 for r in ALL if r["verification"] == "source-doi")
n_unres = sum(1 for r in ALL if r["verification"] == "unresolved")

payload = {
    "schema": "references/v1",
    "citation_style": "IEEE",
    "note": "Primary literature only. verification: 'web' = title/venue/year corroborated "
            "by an independent source during Phase 2; 'source-doi' = DOI/arXiv taken from the "
            "presenters' own curated publication lists (resolvable, not independently re-checked); "
            "'unresolved' = no stable identifier found (batched for the user). Identifiers are "
            "never invented — only those found in a source list or confirmed on the web.",
    "verification_counts": {"web": n_web, "source_doi": n_src, "unresolved": n_unres},
    "sections": {
        "1": "Spatial Perception — Data-Centric AI for Acoustics",
        "2": "Contextual Understanding",
        "3": "Context-Aware Action: Active Noise Control",
        "4": "Context-Aware Action: Soundscape Augmentation",
        "5": "Towards Intelligent Sound Management",
    },
    "counts": {"total": len(ALL), "by_section": by_section},
    "references": ALL,
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT} — {len(ALL)} unique references")
for s in sorted(by_section):
    print(f"  section {s}: {by_section[s]}")
