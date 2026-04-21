#!/usr/bin/env python3
import os
import textwrap
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.image import imread

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "final_report.pdf"))
FIG_DIR = os.path.join(SCRIPT_DIR, "figures")


def _wrap_lines(text, width=105):
    lines = []
    for para in text.split("\n"):
        para = para.rstrip()
        if not para:
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para, width=width))
    return lines


def add_text_page(pdf, heading, body, subheading=None, fontsize=10):
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    y = 0.965
    ax.text(0.07, y, heading, fontsize=16, fontweight="bold", va="top")
    y -= 0.04

    if subheading:
        ax.text(0.07, y, subheading, fontsize=11, style="italic", va="top")
        y -= 0.035

    for line in _wrap_lines(body):
        if y < 0.06:
            pdf.savefig(fig)
            plt.close(fig)
            fig = plt.figure(figsize=(8.27, 11.69))
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis("off")
            y = 0.965
            ax.text(0.07, y, heading + " (contd.)", fontsize=14, fontweight="bold", va="top")
            y -= 0.04

        if line == "":
            y -= 0.012
        else:
            ax.text(0.07, y, line, fontsize=fontsize, va="top")
            y -= 0.019

    pdf.savefig(fig)
    plt.close(fig)


def add_figure_page(pdf, heading, image_path, caption):
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    ax.text(0.07, 0.965, heading, fontsize=16, fontweight="bold", va="top")

    if os.path.exists(image_path):
        img = imread(image_path)
        img_ax = fig.add_axes([0.08, 0.2, 0.84, 0.68])
        img_ax.imshow(img)
        img_ax.axis("off")
        ax.text(0.08, 0.15, caption, fontsize=10, va="top")
    else:
        ax.text(0.08, 0.8, f"Figure missing: {image_path}", fontsize=11, color="red")
        ax.text(0.08, 0.75, caption, fontsize=10, va="top")

    pdf.savefig(fig)
    plt.close(fig)


def build_report():
    with PdfPages(OUT_PDF) as pdf:
        add_text_page(
            pdf,
            "Quantization Effects on Reasoning in Small Language Models",
            """
Final Report (DL23 Project)

Abstract
This report studies how aggressive quantization changes reasoning behavior in a 1.5B model and what recovery methods actually help in practice. The complete workflow is implemented in DL23.ipynb and the quantitative evidence comes from 05_results/. We reproduced baseline versus degradation behavior, adapted QLoRA-style supervised recovery, and extended the project with decoding ablations plus a pilot RL (GRPO) stage. The key finding is practical: in this project, decoding controls and focused supervised adaptation gave stronger and more reliable gains than small-budget RL. We also explain why our RL scope was intentionally reduced and why full BitNet-style training was not feasible under our compute and time budget.

Introduction
Resource-aware deployment requires quantization, but lower precision can disrupt long reasoning chains. This project asks three concrete questions: (1) how much quality is lost when we push toward 4-bit settings, (2) which recovery approach is strongest under realistic constraints, and (3) whether a constrained RL phase gives meaningful benefit beyond supervised finetuning and decoding controls.
            """,
            subheading="Research-paper structure report generated from DL23.ipynb and 05_results artifacts",
        )

        add_text_page(
            pdf,
            "Project Roadmap",
            """
How to read this report quickly:
1) If you want the big picture, read Results + Ablations first.
2) If you care about reproducibility, read Experimental Setup + Limitations.
3) If you care about model behavior, read Failure Cases carefully.

Phase map used in DL23.ipynb:
- Phase 1: 8-bit baseline (reference quality).
- Phase 2: 4-bit degradation measurement.
- Phase 4: QLoRA-style supervised recovery.
- Phase 5: Decoding ablations (inference-time controls).
- Phase 7: Consolidated QLoRA SFT experiments with quant variants.
- Phase 8: Pilot GRPO experiment with strict caps.

Traceability examples from notebook and artifacts:
- Environment printouts: Python 3.13.2, CUDA 12.8, GPU Name: NVIDIA H100 NVL, GPU VRAM: 93.09 GB.
- Package printouts: transformers 5.5.0, trl 0.24.0, peft 0.19.1, accelerate 1.13.0, datasets 4.3.0, bitsandbytes 0.49.2.
- Core result tables: 05_results/main_results.csv and 05_results/ablations.csv.
- Core plots: 05_results/figures/phase6_final_comparison_chart.png and phase7_vs_phase8_plot.png.

            """,
        )

        add_text_page(
            pdf,
            "Related Work",
            """
Primary Paper 1: BitNet [1]
Brief summary: BitNet proposes a 1-bit Transformer direction with BitLinear layers, aiming for strong efficiency gains while preserving language modeling quality.
Influence on our project: BitNet shaped our ambition to push quantization aggressively.
What we actually did: we attempted to move in a BitNet-inspired direction, but full from-scratch 1-bit training was too computationally heavy for our available budget and timeline.

Primary Paper 2: QLoRA [2]
Brief summary: QLoRA shows that a frozen quantized backbone plus trainable LoRA adapters can recover task performance at far lower memory cost.
Influence on our project: this is the central paper we adapted.
Concrete notebook examples:
- Phase 7 requests NF4 and NF4+KV configurations.
- Phase 7 adapter uses r=16, lora_alpha=16, lora_dropout=0, and target modules q_proj/k_proj/v_proj/o_proj/gate_proj/up_proj/down_proj.
- Phase 8 also uses a LoRA adapter with r=16 and NF4-style loading for the base.

Additional Paper 1: Evaluating the Generalization Ability of Quantized LLMs [3]
Brief summary: this work emphasizes that quantized behavior depends on data and evaluation context, and proposes benchmark-centric analysis.
Influence on our project: we avoided single-task conclusions by testing both GSM8K and GPQA and by reporting not only accuracy but also structural failures.
Concrete impact: the same intervention can help one dataset and hurt another; we explicitly show such task dependence in Phase 7 and Phase 8 comparisons.

Additional Paper 2: Interpreting the Effects of Quantization on LLMs [4]
Brief summary: this paper analyzes quantization effects through interpretability and calibration lenses and reports model-dependent outcomes.
Influence on our project: we separate "format is stable" from "answer is correct".
Concrete impact in our raw rows: some predictions keep clean structure and complete answers but still produce wrong final decisions.

Citation verification note:
- BitNet: arXiv:2310.11453
- QLoRA: arXiv:2305.14314
- Quantized generalization benchmark: arXiv:2406.12928
- Quantization interpretability paper: arXiv:2508.16785
            """,
        )

        add_text_page(
            pdf,
            "Methodology",
            """
How we designed the phase logic:
We deliberately organized the project as a sequence of phases instead of one large run. Quantization studies can fail in multiple ways, so splitting the workflow into smaller steps makes it easier to identify what is helping and what is hurting.

Why we chose these phases:
- Phase 1 (reference baseline): we needed a trustworthy starting point to define normal performance before aggressive compression.
- Phase 2 (degradation check): we then lowered precision to measure the direct cost of quantization on accuracy and output stability.
- Phase 4 (supervised recovery): we tested whether lightweight adapter tuning can recover reasoning quality without full-model retraining.
- Phase 5 (decoding recovery): we tested low-cost inference controls to see how much can be recovered without additional training.
- Phase 7 (consolidated supervised study): we ran a structured supervised comparison across quantization styles and both datasets.
- Phase 8 (pilot reinforcement learning): we tested whether reward-driven optimization could improve behavior beyond supervised tuning.

How this appears in DL23 in practical terms:
- The supervised recovery path uses compact adapter training with a small effective batch, accumulation, warm-up, and a capped step budget.
- The supervised evaluation path is kept fixed at 30 examples per dataset to keep comparisons fair and reproducible.
- The pilot RL stage is intentionally small-scale, using a 30-example training subset and 20-example evaluation caps, so feasibility can be tested before larger runs.
- Reward design in the RL pilot starts by encouraging cleaner structure and then increases emphasis on correctness.

Methodological value of this structure:
Each phase isolates one hypothesis: baseline quality, quantization damage, supervised recovery, decoding recovery, and pilot RL effect. That makes the final conclusions easier to interpret and defend.
            """,
        )

        add_text_page(
            pdf,
            "Methodology in Practice",
            """
This is how the phase logic was actually executed in DL23.

Phase 1 in practice: establish the reference
We first run a stronger baseline on both math and science tasks. This confirms that prompts, parsing rules, and metrics are working before we stress the model with lower precision.

Phase 2 in practice: isolate quantization damage
Next, we reduce precision while keeping the task setup as consistent as possible. This lets us attribute drops in accuracy, truncation, and looping to quantization effects rather than unrelated pipeline changes.

Phase 4 in practice: supervised recovery with compact tuning
Instead of expensive full-model retraining, we train lightweight adapters. In DL23 this stage uses a modest step budget and controlled optimization settings so runs stay stable and repeatable.

Phase 5 in practice: decoding as a controllable lever
We then modify only generation behavior (for example deterministic decoding and loop-aware controls). This phase was chosen because it is cheap to run and can produce large quality gains without additional training cost.

Phase 7 in practice: consolidate supervised findings
After early recovery experiments, we run a structured supervised comparison across quantization variants and both datasets. This gives a clean supervised checkpoint before moving into reinforcement learning.

Phase 8 in practice: constrained RL pilot
Finally, we run a pilot reinforcement-learning stage on small train/eval subsets and conservative generation settings. The goal here is directional evidence and feasibility, not a final benchmark claim.

            """,
        )

        add_text_page(
            pdf,
            "Experimental Setup",
            """
Artifacts used:
- Main implementation: DL23.ipynb
- Aggregated metrics: 05_results/main_results.csv
- Ablations: 05_results/ablations.csv
- Comparison plots: 05_results/figures/*.png

Environment and hardware evidence from notebook logs:
- Python 3.13.2, CUDA 12.8.
- Observed run includes NVIDIA H100 NVL (93.09 GB VRAM).
- Notebook project summary also states strict Colab T4-style constraints (16 GB VRAM) as a design driver.

Configuration examples tied to notebook code:
- Phase 7 base model id: unsloth/DeepSeek-R1-Distill-Qwen-1.5B.
- Phase 8 base model id: Qwen/Qwen2.5-1.5B-Instruct.
- Phase 8 quantization config: load_in_4bit=True, quant type NF4, double quantization enabled.
- Phase 8 LoRA config: r=16, lora_alpha=16, lora_dropout=0.05.

Scope reduction due compute/memory/data limits (explicitly justified):
- Phase-8 train caps: GSM8K=2000, GPQA=200.
- Phase-8 eval caps: GSM8K=20, GPQA=20.
- RL trainer used pilot subset: 30 GSM8K rows only.
- Pilot generation controls were conservative (max completion length 64, low generation counts/batch settings).

Additional RL pilot settings from notebook config_candidates:
- per_device_train_batch_size=1
- gradient_accumulation_steps=2
- generation_batch_size=2
- learning_rate=5e-6
- num_generations=2
- num_train_epochs=20

Reason for scope reduction:
These limits were required to keep memory use stable, prevent long unstable multi-generation RL runs, and ensure the team could iterate reproducibly. Therefore, Phase 8 conclusions are correctly reported as pilot-level and not as full RL convergence results.
            """,
        )

        add_text_page(
            pdf,
            "Results",
            """
Main outcomes from 05_results/main_results.csv:

Results table (GSM8K):
| Phase | Setting              | Accuracy % | Truncation % | N |
| P1    | 8-bit baseline       | 76.67      | 0.00         | 30 |
| P2    | 4-bit degraded       | 60.00      | 6.67         | 30 |
| P4    | 4-bit + QLoRA        | 46.67      | 0.00         | 30 |
| P5    | 4-bit + decoding     | 76.67      | 0.00         | 30 |
| P7    | QLoRA SFT average    | 38.33      | 0.00         | 30 |
| P8    | GRPO pilot           | 15.00      | 0.00         | 20 |

Results table (GPQA):
| Phase | Setting              | Accuracy % | Truncation % | N |
| P2    | 4-bit degraded       | 20.00      | 53.33        | 30 |
| P4    | 4-bit + QLoRA        | 26.67      | 13.33        | 30 |
| P5    | 4-bit + decoding     | 36.67      | 26.67        | 30 |
| P7    | QLoRA SFT average    | 20.00      | 13.33        | 30 |
| P8    | GRPO pilot           | 30.00      | 0.00         | 20 |

Interpretation:
1) What quantization breaks:
- GSM8K drops from 76.67 to 60.00 when moving baseline to degraded 4-bit setup.
- GPQA suffers severe truncation in degraded mode (53.33%), indicating output-structure fragility.

2) What recovered quality most efficiently:
- Decoding controls restored GSM8K strongly (for example, greedy logic reaches 76.67 in the main table and 80.00 in decoding ablations).
- On GPQA, decoding loop controls improved from 20.00 baseline decoding to 36.67 for loop breaker 2.

3) Comparative Analysis of Phase 7 and 8:
- Phase 8 GPQA improved over Phase 7 average (30.00 vs 20.00).
- Phase 8 GSM8K underperformed Phase 7 average (15.00 vs 38.33).
- This mixed outcome is expected from a pilot RL setup with tiny training subset and strict generation caps.

Practical takeaway:
If compute is constrained, decoding and targeted SFT are safer first choices; RL should be staged later with larger datasets and longer training.
            """,
        )

        add_figure_page(
            pdf,
            "Results Figure",
            os.path.join(FIG_DIR, "phase6_final_comparison_chart.png"),
            "Figure: Cross-phase comparison chart exported from the notebook workflow.",
        )

        add_figure_page(
            pdf,
            "Phase 7 vs Phase 8",
            os.path.join(FIG_DIR, "phase7_vs_phase8_plot.png"),
            "Figure: Direct comparison of Phase-7 QLoRA SFT and Phase-8 GRPO pilot outcomes.",
        )

        add_text_page(
            pdf,
            "Ablations",
            """
Ablation evidence from 05_results/ablations.csv:

Decoding ablations (Phase 5):
- GSM8K baseline decoding: 66.67%.
- GSM8K greedy logic: 80.00% with 0.00% truncation.
- GPQA baseline decoding: 20.00% with 53.33% truncation.
- GPQA loop breaker 2: 36.67% with 26.67% truncation.

Phase-7 quantization variant ablations:
- GSM8K: NF4=36.67%, NF4+KV=40.00%.
- GPQA: NF4=23.33%, NF4+KV=16.67%.

Ablation takeaway in plain language:
- Not all "more advanced" options help uniformly.
- For GSM8K, straightforward decoding controls gave large upside.
- For GPQA, loop-focused decoding reduced truncation and improved accuracy over baseline decoding.
- Quantization variant benefits are dataset-sensitive (NF4+KV helped GSM8K but hurt GPQA in this run).
            """,
        )

        add_text_page(
            pdf,
            "Ablations with Practical Examples",
            """
Decoding ablation example (GSM8K):
- Baseline decoding: 66.67 accuracy, 3.33 truncation.
- Greedy logic: 80.00 accuracy, 0.00 truncation.
Interpretation: When we changed to a more deterministic decoding style, the model became much more stable. It gave fewer broken outputs and more consistent final answers. This is reflected by the jump in accuracy from 66.67 to 80.00 and the drop in truncation from 3.33 to 0.00.

Decoding ablation example (GPQA):
- Baseline decoding: 20.00 accuracy, 53.33 truncation.
- Loop breaker 2: 36.67 accuracy, 26.67 truncation.
Interpretation: In the science multiple-choice setting, loop-control decoding made a clear difference. It reduced output breakdowns and improved correctness at the same time, which suggests that careful generation controls can recover useful quality even without extra retraining.

Phase 7 quantization variant example:
- gsm8k__nf4 = 36.67, gsm8k__nf4_kv = 40.00.
- gpqa__nf4 = 23.33, gpqa__nf4_kv = 16.67.
Interpretation: The same quantization choice does not behave the same way on every task. One variant helped the math dataset but hurt the science dataset, which means there is no universal "best" setting. The right choice depends on the task you care about.

Important Takeaways:
1) Do not assume one configuration will work best for all tasks.
2) Compare settings task by task before deciding what to deploy.
3) Check both accuracy and failure behavior, because average scores alone can hide important differences.
            """,
        )

        add_figure_page(
            pdf,
            "Phase 7 Metrics",
            os.path.join(FIG_DIR, "phase7_step6_metrics_plot.png"),
            "Figure: Phase-7 metric plot from report artifacts.",
        )

        add_text_page(
            pdf,
            "Failure Cases",
            """
Failure evidence from 05_results/figures/phase8_raw_eval.csv (40 rows total):
- GPQA (20 rows): 30.00% accuracy, 0.00% loop failure, 0.00% truncation.
- GSM8K (20 rows): 15.00% accuracy, 0.00% loop failure, 0.00% truncation.

Representative incorrect cases:
1) GPQA: prediction C vs ground truth B, with long explanation text that sounds plausible but selects the wrong final option.
2) GPQA: prediction A vs ground truth B, where reasoning is verbose but decision grounding is weak.
3) GSM8K: prediction 0 vs ground truth 18; chain-of-thought style text exists, but arithmetic closure fails.

Observed pattern:
The model can produce well-formed responses without being correct. In other words, structural quality and answer correctness are not equivalent.

Why this section is important:
- Aggregate metrics alone can hide these behaviors.
- Failure examples explain why Phase 8 can show zero loop/truncation failures but still have low GSM8K accuracy.
            """,
        )

        add_text_page(
            pdf,
            "Failure Analysis: What to Do Next",
            """
Failure mode 1: Option selection drift in science multiple-choice questions
In several science examples, the model produced long and confident reasoning but still selected the wrong final option letter. This is important because the output can look "thoughtful" while still being incorrect at the decision step. In other words, the model is not always failing at reasoning structure, but it is failing at final answer calibration.

What this likely means:
The model may understand parts of the question but does not consistently map that reasoning to the correct final option token.

What we should do next:
We should add a stronger reward signal for final-option correctness and enforce consistency checks between the final answer letter and the reasoning summary. This will help align "reasoning quality" with "decision quality."

Failure mode 2: Arithmetic closure errors in math questions
In multiple math rows, the model followed a seemingly sensible chain of steps but ended with the wrong final number. This indicates a "last-step failure" pattern: most of the reasoning is acceptable, but the final arithmetic closure is not reliable.

What this likely means:
The model can preserve procedural reasoning language, yet still lose precision in the final computation or answer extraction stage.

What we should do next:
We should add stronger numeric-consistency rewards, plus a lightweight post-generation arithmetic verifier that checks whether the final number is consistent with the intermediate reasoning. This is a practical way to improve reliability without retraining the entire system from scratch.

Failure mode 3: Generic fallback language replacing precise logic
Some outputs become overly generic, hesitant, or apologetic instead of concluding with a precise decision. This lowers usefulness, especially in tasks where the expected output is a clear number or a clear option letter.

What this likely means:
When the model is uncertain, it may default to safe but low-information language rather than committing to the most evidence-backed answer.

What we should do next:
We should penalize low-information fallback phrasing and reward concise, task-appropriate final answers. That makes the model less likely to "sound safe" while avoiding the real task.

Practical extension plan linked to this notebook:
1) Increase the generation-length cap for tasks that require longer multi-step reasoning, so valid chains are not cut short.
2) Expand the reinforcement-learning training subset beyond a tiny pilot size and include both task types, not only one domain.
3) Re-run evaluation with broader sample caps so the conclusions are less sensitive to small-sample variance.

Overall interpretation:
The current pilot already shows where the model fails and why. That is valuable. These failure signatures are concrete enough to guide the next training cycle, and they point to targeted improvements rather than blind scaling.
            """,
        )

        add_text_page(
            pdf,
            "Limitations",
            """
1) Compute and memory constraints forced strict caps, reduced subset sizes, and pilot-only RL.
2) The RL stage was not trained at full scale across full datasets, so no full-convergence claim is made.
3) Reduced sample counts increase estimate variance and reduce statistical confidence.
4) We attempted BitNet-style implementation directionally, but full from-scratch 1-bit training was too computationally heavy for our setup.
5) Results are specific to this project stack (model family, prompting style, and pipeline details in DL23.ipynb).

More explicit scope-reduction rationale:
- The project balanced research breadth against finite budget. We prioritized phase-by-phase, testable progress over one expensive experiment that could fail without diagnostics.
- This is why Phase 8 is framed as pilot evidence, not a final RL verdict.
- This is also why BitNet is discussed as studied and attempted, but not claimed as fully reproduced.

Despite these limits, the study still provides actionable evidence: quantization degradation is measurable, decoding-time controls can be high leverage, and constrained RL needs more budget and broader data coverage before strong claims.
            """,
        )

        add_text_page(
            pdf,
            "Conclusion",
            """
What we can confidently say from this project:
1) Quantization can significantly damage reasoning quality and output stability, especially on harder science-style QA.
2) Recovery is possible, but not all recovery methods are equally cost-effective.
3) In this project, decoding controls and compact supervised adaptation delivered stronger practical gains than small-budget RL.

What we cannot claim yet:
- We cannot claim full RL effectiveness because Phase 8 was intentionally pilot-scoped.
- We cannot claim BitNet reproduction because full from-scratch 1-bit training was beyond budget.
            """,
        )

        add_text_page(
            pdf,
            "References",
            """
[1] Hongyu Wang, Shuming Ma, Li Dong, Shaohan Huang, Huaijie Wang, Lingxiao Ma, Fan Yang, Ruiping Wang, Yi Wu, and Furu Wei. BitNet. arXiv:2310.11453 (2023).

[2] Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. QLoRA: Efficient Finetuning of Quantized LLMs. arXiv:2305.14314 (2023).

[3] Yijun Liu, Yuan Meng, Fang Wu, Shenhao Peng, Hang Yao, Chaoyu Guan, Chen Tang, Xinzhu Ma, Zhi Wang, and Wenwu Zhu. Evaluating the Generalization Ability of Quantized LLMs: Benchmark, Analysis, and Toolbox. arXiv:2406.12928 (2024).

[4] Manpreet Singh and Hassan Sajjad. Interpreting the Effects of Quantization on LLMs. arXiv:2508.16785 (2025).
            """,
        )

    print(f"Built fallback report: {OUT_PDF}")


if __name__ == "__main__":
    build_report()
