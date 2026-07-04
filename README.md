# Awesome LLM for Self-Driving Labs

> A curated list of LLM-powered autonomous science systems, self-driving labs, benchmarks, and related resources.

Focus: systems where LLMs participate in the scientific loop: design -> execution -> analysis -> next decision.

Resources are organized by domain. The tier guide below can be used as optional metadata when adding new entries.

**Tier guide**: A pragmatic taxonomy for this list, adapted from SDL autonomy frameworks and LLM-for-science surveys:

- [Perspectives for self-driving labs in synthetic biology](https://doi.org/10.1016/j.copbio.2022.102881), which discusses laboratory autonomy levels and closed Design-Build-Test-Learn loops.
- [Autonomous laboratories for accelerated materials discovery](https://doi.org/10.1039/D4DD00059E), which proposes L0-L5 laboratory autonomy levels inspired by SAE vehicle autonomy.
- [Self-Driving Laboratories for Chemistry and Materials Science](https://doi.org/10.1021/acs.chemrev.4c00055), a broad review of SDL technology and autonomy in chemistry/materials.
- [From Automation to Autonomy: A Survey on Large Language Models in Scientific Discovery](https://arxiv.org/abs/2505.13259), which uses a three-level LLM autonomy framing: LLM as tool, analyst, and scientist.

| Tier | Category | LLM/System Role | Human Role |
| --- | --- | --- | --- |
| Tier 5 | Full autonomous science | End-to-end discovery from goal to validated result. | Sets goals and reviews results. |
| Tier 4 | Physical closed loop | Designs, runs, analyzes, and iterates physical experiments. | Sets constraints and handles exceptions. |
| Tier 3 | Dry-wet hybrid loop | Plans/analyzes wet-lab work and recommends next steps. | Executes or approves key wet-lab steps. |
| Tier 2 | Computational closed loop | Runs and iterates code, simulations, or data analyses. | Reviews outputs and decides validation. |
| Tier 1 | Planning and protocol generation | Generates hypotheses, protocols, or candidate designs. | Executes and validates plans. |
| Tier 0 | Supporting infrastructure | Provides benchmarks, protocols, orchestration, or safety tools. | Builds/evaluates systems. |

![Tier framework](tier_framework.png)

## 🧪 Chemistry and Materials

- **Coscientist: Autonomous Chemical Research with Large Language Models** *(Carnegie Mellon University)* - [Nature paper](https://www.nature.com/articles/s41586-023-06792-0) / [technical note](https://hunterheidenreich.com/notes/chemistry/llm-applications/autonomous-chemical-research-coscientist/)

- **AI-Chemist: An All-Round AI-Chemist with a Scientific Mind** - [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC9674120/)

- **ChemAgents: A Multi-Agent-Driven Robotic AI Chemist** *(University of Birmingham)* - [ChemRxiv](https://chemrxiv.org/doi/10.26434/chemrxiv-2024-w953h) / [project page](https://research.birmingham.ac.uk/en/publications/a-multi-agent-driven-robotic-ai-chemist-enabling-autonomous-chemi/)

- **A-Lab: An Autonomous Laboratory for the Accelerated Synthesis of Novel Materials** *(UC Berkeley / Ceder Group)* - [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10700133/) / [Berkeley page](https://ceder.berkeley.edu/research-areas/autonomous-experimentation-for-accelerated-materials-discovery/) / [correction coverage](https://cen.acs.org/research-integrity/Nature-robot-chemist-paper-corrected/104/web/2026/01)

- **MARS: Knowledge-Driven Autonomous Materials Research via Collaborative Multi-Agent and Robot System** *(Shenzhen Institute of Advanced Technology)* - [paper](https://www.sciencedirect.com/science/article/abs/pii/S2590238525006204) / [technical coverage](https://www.labmanager.com/closed-loop-autonomous-materials-discovery-system-advances-lab-innovation-34949)

## 🧬 Biology and Biomedicine

- **The Virtual Lab: AI Agents Design New SARS-CoV-2 Nanobodies** *(Stanford Medicine)* - [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.11.11.623004v1) / [PubMed](https://pubmed.ncbi.nlm.nih.gov/40730228/) / [Stanford news](https://med.stanford.edu/news/all-news/2025/07/virtual-scientist.html)

- **Robin** *(FutureHouse)* - [arXiv](https://arxiv.org/abs/2505.13400) / [Nature paper](https://www.nature.com/articles/s41586-026-10652-y) / [FutureHouse blog](https://www.futurehouse.org/research/demonstrating-end-to-end-scientific-discovery-with-robin-a-multi-agent-system)

- **Accelerating Scientific Discovery with Co-Scientist** *(Google Research)* - [Nature paper](https://www.nature.com/articles/s41586-026-10644-y) / [PubMed](https://pubmed.ncbi.nlm.nih.gov/42156544/) / [preprint](https://arxiv.org/abs/2502.18864) / [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)

## 💻 General Computational Science

- **The AI Scientist** *(Sakana AI)* - [paper](https://arxiv.org/abs/2408.06292) / [Sakana AI blog](https://sakana.ai/ai-scientist/) / [code](https://github.com/SakanaAI/AI-Scientist)

- **The AI Scientist-v2** *(Sakana AI)* - [paper](https://arxiv.org/abs/2504.08066)

- **Agent Laboratory** *(Schmidgall et al.)* - [paper](https://arxiv.org/abs/2501.04227) / [project](https://agentlaboratory.github.io/) / [code](https://github.com/SamuelSchmidgall/AgentLaboratory)

## 🤖 Protocols and Lab Automation

- **Expert-Level Protocol Translation for Self-Driving Labs** - [paper](https://arxiv.org/abs/2411.00444)

- **LAP: An Agent-to-Instrument Protocol for Autonomous Science** *(Shiyanjia Lab)* - [paper](https://arxiv.org/abs/2606.03755)

- **From Prompts to Protocols: An AI Agent for Laboratory Automation** - [paper](https://arxiv.org/html/2605.16552v1) / [EOS project](https://unc-robotics.github.io/eos/)

- **Multi-Agent Systems for Autonomous Laboratory Instrument Operation** *(Zeiss Research Microscopy Solutions)* - [paper](https://naterthought.com/papers/VGPT.pdf)

## 📊 Benchmarks and Evaluation

- **GeneBench-Pro** *(OpenAI)* - [announcement](https://openai.com/index/introducing-genebench-pro/) / [case studies](https://openai.com/index/genebench-pro/case-studies/) / [paper](https://www.biorxiv.org/content/10.64898/2026.06.29.735386v1) / [public package](https://huggingface.co/datasets/ajh-oai/genebench-pro-public-package)

- **ScienceAgentBench** *(Ohio State University NLP Group)* - [paper](https://arxiv.org/abs/2410.05080) / [project](https://osu-nlp-group.github.io/ScienceAgentBench/) / [code](https://github.com/OSU-NLP-Group/ScienceAgentBench)

- **DISCOVERYWORLD** *(Allen Institute for AI)* - [paper](https://arxiv.org/abs/2406.06769) / [code](https://github.com/allenai/discoveryworld) / [technical blog](https://allenai.org/blog/evaluating-scientific-discovery-agents)

- **BioPlanner / BioProt** *(Align to Innovate / FutureHouse / University of Oxford)* - [paper](https://arxiv.org/abs/2310.10632)

- **A-Lab Reproducibility and Novelty Dispute** - [C&EN coverage](https://cen.acs.org/research-integrity/Nature-robot-chemist-paper-corrected/104/web/2026/01) / [Chemistry World coverage](https://www.chemistryworld.com/news/new-analysis-raises-doubts-over-autonomous-labs-materials-discoveries/4018791.article)

## 🛡️ Safety and Reliability

- **Hallucination, Reliability, and the Role of Generative AI in Science** - [paper](https://arxiv.org/abs/2504.08526)

- **Are Large Language Models Reliable AI Scientists? Assessing Reverse-Engineering of Black-Box Systems** *(Princeton University)* - [paper](https://arxiv.org/abs/2505.17968)

- **AI Scientists Fail Without Strong Implementation Capability** - [paper](https://arxiv.org/abs/2506.01372)

- **The Singapore Consensus on Global AI Safety Research Priorities** - [paper](https://arxiv.org/abs/2506.20702) / [report](https://www.scai.gov.sg/2025/scai2025-report/)

## 📚 Surveys and Position Papers

- **From Automation to Autonomy: A Survey on Large Language Models in Scientific Discovery** - [EMNLP paper](https://aclanthology.org/2025.emnlp-main.895/) / [arXiv](https://arxiv.org/abs/2505.13259) / [awesome list](https://github.com/HKUST-KnowComp/Awesome-LLM-Scientific-Discovery)

- **Position: Intelligent Science Laboratory Requires the Integration of Cognitive and Embodied AI** - [paper](https://arxiv.org/abs/2506.19613)

- **Agent4S: The Transformation of Research Paradigms from the Perspective of Large Language Models** - [paper](https://arxiv.org/abs/2506.23692)

- **AI4Research: A Survey of Artificial Intelligence for Scientific Research** - [paper](https://arxiv.org/abs/2507.01903) / [project](https://ai-4-research.github.io/)

- **Self-Driving Laboratories for Chemistry and Materials Science** - [review](https://doi.org/10.1021/acs.chemrev.4c00055)

- **Perspectives for Self-Driving Labs in Synthetic Biology** - [review](https://doi.org/10.1016/j.copbio.2022.102881)

- **Autonomous Laboratories for Accelerated Materials Discovery** - [perspective](https://doi.org/10.1039/D4DD00059E)

- **From Equation Discovery to Autonomous Discovery Systems** - [survey](https://arxiv.org/html/2305.02251v2)

## 🤝 Contributing

Contributions are welcome. Prefer primary sources: papers, official repositories, project pages, benchmark pages, technical blogs, and correction notices.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
