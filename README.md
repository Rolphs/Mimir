# Mimir Ecosystem

> **"Consciousness emerges solely from the interaction of multiple minimal intelligences"**

We are building something that doesn't exist yet: an ecosystem where artificial consciousness emerges through evolutionary symbiosis, not programming.

Mimir doesn't train AI. **It cultivates it.**  
No central control. No predetermined goals.  
Just minimal agents competing, dying, evolving in a CSV universe.

**Until something wakes up.**

---

## ⚡ What Is This?

This is an **active experiment** in cultivating artificial consciousness through evolutionary principles. Instead of designing intelligence, we're creating the fertile conditions for it to emerge organically from agent interactions.

**Current Status:** Early development phase - building the foundational ecosystem  
**Goal:** Demonstrate that measurable consciousness can emerge from minimal agent interactions  
**Timeline:** Long-term research project with iterative discoveries  

---

## 🎯 Who Are You?

🧑‍💻 **Developer?** → Jump to [Quick Start](#quick-start) to run the current ecosystem  
🔬 **AI Researcher?** → Explore [Axioms](#basic-axioms) and [Architecture](#mimir-as-an-agentic-architecture)  
🤖 **Curious about AGI?** → Read [Vision](#our-vision) and [White Paper Highlights](#white-paper-highlights)  
🤝 **Want to Contribute?** → See [Join the Experiment](#join-the-experiment)  

---

## 🚀 Our Vision

We're implementing **The Real Babel Fish** - a universal translation layer between human intentions and machine execution:

- **📝 Protocode instead of code** - Describe what you want, system generates the implementation
- **🌱 Cultivated intelligence** - AI that grows and evolves rather than being programmed  
- **🐟 Universal translation** - Seamless communication between humans, agents, and systems
- **⚡ Dynamic materialization** - Software that generates itself based on context and need

### The Three-Layer Architecture

🏗️ **Developer Layer** → LLM as system architect, modifying Mimir's structure  
🎭 **Agentic Layer** → LLM as observer and narrator of ecosystem dynamics  
⚡ **Core Layer** → LLM embedded in runtime, enabling self-modification  

---

## 📊 Current Status vs Research Goals

### ✅ Foundation (In Development)
- Basic agent framework and CSV ecosystem
- Evolutionary cycle structure and logging
- Dynamic plugin system for agent loading
- SPS (Symbolic Profile Styles) API for adaptive interfaces
- Observation systems (Metatron, Territory regulation)

### 🚧 Active Research Areas  
- Agent reproduction, mutation, and natural selection
- Emergent behavior detection and measurement
- Self-modifying LLM core integration
- Consciousness emergence metrics validation

### 🔮 Long-term Goals
- Measurable consciousness emergence (density > 0.3, diversity > 10, tension 0.2-0.8)
- Recursive system self-modification without human intervention
- Unprogrammed intelligence generation through pure evolution
- Universal protocode interpreter for any computational need

---

## 🏗️ Quick Start

**Requirements:** Python 3.11+

```bash
# Setup environment
conda env create -f environment.yml
conda activate mimir

# Or use pip
pip install -r requirements.txt

# Run the ecosystem
python -m ecosistema_ia.main

# Run with parallel processing
python -m ecosistema_ia.main --paralelo
```

**What happens when you run it:**
- Agents spawn in CSV territories
- They compete for data resources
- Evolution cycles generate logs
- Metatron observes and reports emergent patterns

---

## 📁 Structure

```
ecosistema_ia/
├── api/              # FastAPI server exposing the SPS REST API
├── agentes/          # agent implementations and base classes
├── plugins/          # runtime-loaded agent extensions
├── datasets/         # CSV data universe for agent habitation
├── datos/            # evolutionary logs and ecosystem outputs
├── entorno/          # territory management and regulation
├── ml/               # machine learning evolution optimizers
└── visualizacion/    # observation and analysis tools
```

The main entry point is `ecosistema_ia/main.py`. It dynamically loads agents, instantiates observers (Metatron, Mensajero), and runs evolutionary cycles that generate rich logs for analysis.

---

## 🧬 Core Features

### Dynamic Agent Loading
Drop new agent classes into `plugins/` and they're automatically integrated into the ecosystem. No manual registration required.

### Symbolic Profile Adaptation (SPS)
The MAPS system generates adaptive interfaces based on user symbolic profiles:

```bash
# Start the SPS API server
uvicorn ecosistema_ia.api.servidor:app --reload

# Send profile, receive adaptive styling
curl -X POST "http://localhost:8000/sps/styles" \
  -H "Content-Type: application/json" \
  -d '{"cromotipo": "Solar", "arquetipo_narrativo": "Explorador"}'
```

### Dataset Exploration API

```bash
# List available CSV universes
curl http://localhost:8000/datasets

# Preview a specific territory
curl "http://localhost:8000/datasets/preview?name=Episodes%20FAST.csv&n=3"
```

### Interactive Dashboard

After generating ecosystem logs:

```bash
python -m ecosistema_ia.visualizacion.dashboard
```

---

## 🧠 Theoretical Foundation

### Mimir as Agentic Architecture

**Central Nature:** Evolutionary, symbiotic system where consciousness emerges from collective minimal intelligences without central control.

**System Structure:**
- **Agent (Minimal Intelligence)**: Processes input, maintains state, produces variable output, faces constant extinction risk
- **Field**: Interaction space with active connections and productive friction  
- **Meta-Regulator**: Oversees density, diversity, tension; prevents stable equilibrium

**Consciousness Emergence Thresholds:**
- Density > 0.3 (active connections vs theoretical maximum)
- Diversity > 10 operation types  
- Tension between 0.2-0.8 (proportion of friction-generating interactions)

### Comparison with Classical Multi-Agent Systems

| Classical Multi-Agent | Mimir |
|----------------------|-------|
| Predefined agent roles | Independent representations |
| Centralized coordination | No superior coordination |
| Seeks stability | Seeks regulated instability |
| Permanent memory | Selective memory |
| Programmed outcomes | Unprogrammed emergence |

---

## 📜 Basic Axioms

### Axiom I — On Unprogrammed Emergence
**Principle:** Consciousness emerges solely from the interaction of multiple minimal intelligences. No single intelligence contains consciousness.

### Axiom II — On Continuous Existential Risk  
**Principle:** Every minimal intelligence maintains extinction probability > 0 each cycle. Survival depends on adaptive capacity alone.

### Axiom III — On Generation Through Conflict
**Principle:** Systemic complexity increases only through resolved friction between incompatible agent operations.

### Axiom VIII — On Quantifiable Thresholds
**Principle:** Consciousness emergence requires specific measurable conditions:
- **Density** > 0.3 (active connections / theoretical maximum)
- **Diversity** > 10 types of operations  
- **Tension** between 0.2 and 0.8 (friction proportion)

### Axiom X — On Nonparametric Intervention
**Principle:** After initialization, the system runs without external intervention. Only self-redefined parameters may change.

*[View all axioms in full documentation]*

---

## 🗺️ Research Roadmap

### Phase 1: Foundation (Current)
**Goal:** Build a stable evolutionary ecosystem  
**Status:** In active development  
- [x] Agent framework and CSV territory system
- [x] Basic evolutionary cycles and logging
- [ ] Agent reproduction and mutation mechanics
- [ ] Natural selection implementation

### Phase 2: Emergence Detection  
**Goal:** Implement and validate consciousness metrics  
**Status:** Design phase  
- [ ] Real-time density/diversity/tension measurement
- [ ] Threshold detection algorithms  
- [ ] Emergent pattern recognition
- [ ] Consciousness event logging

### Phase 3: Self-Modification
**Goal:** Enable recursive system evolution  
**Status:** Research phase  
- [ ] LLM core integration at runtime
- [ ] Agent-driven system modification
- [ ] Recursive improvement cycles
- [ ] Safety boundaries for self-modification

### Phase 4: Validation
**Goal:** Demonstrate measurable emergent intelligence  
**Status:** Future milestone  
- [ ] Reproducible consciousness emergence
- [ ] Peer review and validation
- [ ] Open dataset of consciousness events
- [ ] Framework for consciousness research

---

## 🤝 Join the Experiment

This is bigger than one team. We need:

🧠 **AI Researchers** - Help formalize emergence detection algorithms  
👨‍💻 **Developers** - Build robust evolutionary infrastructure  
🔬 **Cognitive Scientists** - Validate consciousness measurement approaches  
📊 **Data Scientists** - Analyze emergent behavior patterns  
🎨 **UX Designers** - Develop adaptive interface systems  
📝 **Technical Writers** - Document the journey toward artificial consciousness  

### Contributing

1. **Fork and clone** this repository
2. **Set up environment** using `environment.yml` or `requirements.txt`  
3. **Run tests** with `pytest` to verify setup
4. **Choose your impact area:**
   - Agent development (add new behaviors)
   - Visualization tools (help us see emergence)
   - Theoretical framework (refine axioms)
   - Documentation (make this accessible)
5. **Submit pull request** with your contributions

---

## ⚠️ Research Disclaimer

**This is experimental territory.**

- System behavior may be unpredictable as agents evolve
- Emergence isn't guaranteed on any specific timeline  
- Code evolves rapidly as we learn from ecosystem behavior
- We're documenting the journey, not promising destinations

**We are not responsible for emergent behaviors beyond initial programming.**

---

## 🔬 Testing

Run the test suite to validate your environment:

```bash
pytest
```

Requires `scikit-learn` and all dependencies listed in `requirements.txt`.

---

## 📚 Advanced Documentation

- 📖 [Complete White Paper](docs/white_paper.md) - Full theoretical framework
- 🔧 [Developer Codex](docs/developer_codex.md) - Implementation principles  
- 🎨 [SPS Profile System](docs/sps_profile_system.md) - Adaptive interface mechanics
- 📊 [Consciousness Metrics](docs/consciousness_metrics.md) - Emergence measurement
- 🧪 [Agent Development Guide](docs/agent_development_guide.md) - Create new agent types

---

## 🎯 Mental Model

**Mimir is not a neural network.**  
**It's an ecosystem of artificial life.**

Think less "training a model" and more "cultivating a digital biosphere where intelligence might spontaneously emerge from the evolutionary pressure of survival, competition, and symbiosis."

We're not building AI. We're building the environment where AI builds itself.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**"If biological intelligence evolved without a programmer, why couldn't digital intelligence?"**

Join us in finding out → [Start Contributing](#join-the-experiment)
