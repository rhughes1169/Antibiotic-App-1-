import streamlit as st
import random
import graphviz

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Antibiotic Master Visual", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR VISUALS ---
st.markdown("""
<style>
    /* Bigger buttons for iPad */
    div.stButton > button {
        width: 100%;
        height: 3em;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
    }
    /* Card styling */
    div.stContainer {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA SOURCE ---
drug_database = [
    # PENICILLINS
    {"class": "Natural Penicillins", "drugs": "Penicillin G, Penicillin V", "spectrum": "Gram(+) Narrow: Strep, Syphilis.", "adrs": "Seizures (high dose), Hypersensitivity.", "notes": "Susceptible to Beta-Lactamases."},
    {"class": "Anti-Staphylococcal Penicillins", "drugs": "Nafcillin, Oxacillin, Dicloxacillin", "spectrum": "MSSA, Strep.", "adrs": "Nafcillin = Phlebitis/Neutropenia.", "notes": "Biliary excretion (Nafcillin). For MSSA only."},
    {"class": "Aminopenicillins", "drugs": "Ampicillin, Amoxicillin", "spectrum": "Gram(+) + H.E.L.P (H. flu, E. coli, Listeria, Proteus).", "adrs": "Rash (Mono), Diarrhea.", "notes": "Pair with BL-inhibitors (Clavulanate)."},
    {"class": "Antipseudomonal Penicillins", "drugs": "Piperacillin, Ticarcillin", "spectrum": "Gram(-) Pseudomonas, Klebsiella.", "adrs": "Bleeding/Platelet dysfunction.", "notes": "Used as Pip/Tazo."},
    # CEPHALOSPORINS
    {"class": "1st Gen Cephalosporins", "drugs": "Cefazolin, Cephalexin, Cefadroxil", "spectrum": "Gram(+) + PEcK.", "adrs": "Cross-allergy Penicillins.", "notes": "Surgical prophylaxis (Cefazolin)."},
    {"class": "2nd Gen Cephalosporins", "drugs": "Cefuroxime, Cefoxitin, Cefotetan", "spectrum": "Gram(+) + HEN PEcK.", "adrs": "Cefotetan: Disulfiram rxn, Bleeding.", "notes": "Anaerobes (Cefoxitin/Cefotetan)."},
    {"class": "3rd Gen Cephalosporins", "drugs": "Ceftriaxone, Ceftazidime, Cefotaxime, Cefdinir", "spectrum": "Gram(-) Heavy. Meningitis.", "adrs": "Biliary Sludging (Ceftriaxone).", "notes": "Ceftazidime = Pseudomonas coverage."},
    {"class": "4th Gen Cephalosporins", "drugs": "Cefepime", "spectrum": "Broad: Gram(+) & Gram(-) & Pseudo.", "adrs": "Neurotoxicity.", "notes": "Zwitterion (penetrates well)."},
    {"class": "5th Gen Cephalosporins", "drugs": "Ceftaroline", "spectrum": "Anti-MRSA.", "adrs": "Standard.", "notes": "Binds PBP2a."},
    # OTHERS
    {"class": "Carbapenems", "drugs": "Imipenem, Meropenem, Ertapenem", "spectrum": "Broadest (Anaerobes+Pseudo).", "adrs": "Seizures (Imipenem).", "notes": "Ertapenem misses Pseudomonas/Acinetobacter."},
    {"class": "Monobactams", "drugs": "Aztreonam", "spectrum": "Gram(-) Aerobes ONLY.", "adrs": "Safe in Penicillin allergy.", "notes": "Zero Gram(+) activity."},
    {"class": "Glycopeptides", "drugs": "Vancomycin", "spectrum": "Gram(+) ONLY (MRSA).", "adrs": "Red Man Syn, Nephro/Oto-toxicity.", "notes": "Binds D-Ala-D-Ala."},
    {"class": "Lipopeptides", "drugs": "Daptomycin", "spectrum": "Gram(+) MRSA/VRE.", "adrs": "Myopathy (CPK).", "notes": "Inactivated by lung surfactant."},
    {"class": "Others", "drugs": "Fosfomycin", "spectrum": "UTI organisms.", "adrs": "GI upset.", "notes": "Inhibits MurA."}
]

quiz_bank = [
    {
        "q": "Target: D-Ala-D-Ala. Drug?", 
        "opt": ["Vancomycin", "Penicillin", "Daptomycin"], 
        "ans": "Vancomycin", 
        "expl": "Vancomycin binds the D-Ala-D-Ala tail."
    },
    {
        "q": "Patient has Pseudomonas. Penicillin allergy (Anaphylaxis). Safe choice?", 
        "opt": ["Piperacillin", "Cefepime", "Aztreonam"], 
        "ans": "Aztreonam", 
        "expl": "Monobactams have no cross-reactivity."
    },
    {
        "q": "Which drug is inactivated by Lung Surfactant?", 
        "opt": ["Daptomycin", "Linezolid", "Ceftaroline"], 
        "ans": "Daptomycin", 
        "expl": "Daptomycin cannot treat pneumonia."
    },
    {
        "q": "Drug causing 'Red Man Syndrome'?", 
        "opt": ["Vancomycin", "Nafcillin", "Cefotetan"], 
        "ans": "Vancomycin", 
        "expl": "Histamine release due to rapid infusion."
    },
    {
        "q": "Only Cephalosporin active against MRSA?", 
        "opt": ["Ceftaroline", "Cefepime", "Ceftriaxone"], 
        "ans": "Ceftaroline", 
        "expl": "5th Gen Ceftaroline binds PBP2a."
    },
    {
        "q": "3rd Gen Cephalosporin that covers Pseudomonas?", 
        "opt": ["Ceftazidime", "Ceftriaxone", "Cefotaxime"], 
        "ans": "Ceftazidime", 
        "expl": "Ceftazidime is the specific 3rd gen for Pseudomonas."
    }
]

# --- SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'total_q' not in st.session_state: st.session_state.total_q = 0
if 'flash_idx' not in st.session_state: st.session_state.flash_idx = 0
if 'reveal' not in st.session_state: st.session_state.reveal = False

# --- SIDEBAR ---
with st.sidebar:
    st.header("📊 Study Stats")
    st.metric("Quiz Score", f"{st.session_state.score} / {st.session_state.total_q}")
    if st.button("Reset Score"):
        st.session_state.score = 0
        st.session_state.total_q = 0
        st.rerun()
    st.info("💡 Tip: Use the 'Visual Maps' tab to see how these drugs relate.")

# --- MAIN APP ---
st.title("🦠 Antibiotic Master: Visual Edition")

tabs = st.tabs(["🗺️ Visual Maps", "⚡ Flashcards", "🧠 Interactive Quiz", "📚 Library"])

# --- TAB 1: VISUAL MAPS (DIAGRAMS) ---
with tabs[0]:
    st.header("Interactive Mechanism Maps")
    st.caption("Zoomable diagrams generated from your PDF notes.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Mechanism of Action")
        # Graphviz code to visualize MOA
        moa_graph = graphviz.Digraph()
        moa_graph.attr(rankdir='TB')
        
        moa_graph.node('A', 'Cytoplasm: Precursor Synthesis', shape='box', style='filled', fillcolor='lightgrey')
        moa_graph.node('B', 'Cell Membrane', shape='box', style='filled', fillcolor='lightblue')
        moa_graph.node('C', 'Periplasm/Cell Wall', shape='box', style='filled', fillcolor='lightyellow')
        
        moa_graph.edge('A', 'B', label='Transport')
        moa_graph.edge('B', 'C', label='Polymerization')
        
        # Drugs
        moa_graph.node('Fos', 'FOSFOMYCIN', shape='ellipse', style='filled', fillcolor='#ffcccc')
        moa_graph.edge('Fos', 'A', label='Inhibits MurA\n(Early Step)')
        
        moa_graph.node('Dap', 'DAPTOMYCIN', shape='ellipse', style='filled', fillcolor='#ffcccc')
        moa_graph.edge('Dap', 'B', label='Depolarizes\nMembrane')
        
        moa_graph.node('Vanc', 'VANCOMYCIN', shape='ellipse', style='filled', fillcolor='#ffcccc')
        moa_graph.edge('Vanc', 'C', label='Binds D-Ala-D-Ala\n(Blocks Polymerization)')
        
        moa_graph.node('Beta', 'BETA-LACTAMS\n(Penicillins, Cephs, Carbs)', shape='ellipse', style='filled', fillcolor='#ffcccc')
        moa_graph.edge('Beta', 'C', label='Binds PBP\n(Blocks Cross-linking)')
        
        st.graphviz_chart(moa_graph, use_container_width=True)
        st.info("**Visual Note:** Notice how Fosfomycin works inside, Daptomycin on the membrane, and Vanc/Beta-Lactams outside in the wall.")

    with col2:
        st.subheader("2. Cephalosporin Generations")
        # Graphviz for Cephalosporins
        ceph_graph = graphviz.Digraph()
        
        ceph_graph.node('1', '1st Gen\n(Cefazolin)', shape='box')
        ceph_graph.node('2', '2nd Gen\n(Cefuroxime)', shape='box')
        ceph_graph.node('3', '3rd Gen\n(Ceftriaxone)', shape='box')
        ceph_graph.node('3P', '3rd Gen Anti-Pseudo\n(Ceftazidime)', shape='box', style='filled', fillcolor='lightyellow')
        ceph_graph.node('4', '4th Gen\n(Cefepime)', shape='box', style='filled', fillcolor='lightgreen')
        ceph_graph.node('5', '5th Gen\n(Ceftaroline)', shape='box', style='filled', fillcolor='orange')
        
        ceph_graph.edge('1', '2', label='Add HEN (H.flu, Enterobacter, Neisseria)')
        ceph_graph.edge('2', '3', label='Better Gram(-), CNS penetration')
        ceph_graph.edge('3', '3P', label='Add Pseudomonas')
        ceph_graph.edge('3P', '4', label='Add Gram(+)')
        ceph_graph.edge('4', '5', label='Lose Pseudo\nAdd MRSA')
        
        st.graphviz_chart(ceph_graph, use_container_width=True)
        st.info("**Visual Note:** 4th Gen is the broadest (Green). 5th Gen is special for MRSA (Orange) but loses Pseudomonas.")

# --- TAB 2: FLASHCARDS (Interactive) ---
with tabs[1]:
    st.subheader("⚡ Active Recall")
    
    card = drug_database[st.session_state.flash_idx]
    
    # Card UI
    with st.container():
        st.markdown(f"<h2 style='text-align: center; color: #333;'>{card['class']}</h2>", unsafe_allow_html=True)
        st.divider()
        
        if st.session_state.reveal:
            col_a, col_b = st.columns(2)
            with col_a:
                st.success(f"**💊 Drugs:** {card['drugs']}")
                st.info(f"**🦠 Spectrum:** {card['spectrum']}")
            with col_b:
                st.warning(f"**⚠️ ADRs:** {card['adrs']}")
                st.error(f"**📝 Note:** {card['notes']}")
        else:
            st.markdown("<div style='text-align: center; padding: 50px;'><i>Tap Reveal to Flip</i></div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Interaction Buttons
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("👁️ Reveal"):
            st.session_state.reveal = True
            st.rerun()
    with c3:
        if st.button("➡️ Next Card"):
            st.session_state.flash_idx = random.randint(0, len(drug_database)-1)
            st.session_state.reveal = False
            st.rerun()

# --- TAB 3: QUIZ (With Score) ---
with tabs[2]:
    st.subheader("🧠 Clinical Cases")
    
    # Randomly serve a question
    if 'current_q' not in st.session_state:
        st.session_state.current_q = random.choice(quiz_bank)
        st.session_state.q_answered = False
        st.session_state.user_opt = None

    q = st.session_state.current_q
    
    st.markdown(f"**Question:** {q['q']}")
    
    # Display options
    choice = st.radio("Select:", q['opt'], key="quiz_radio", index=None)
    
    submit = st.button("Submit Answer")
    
    if submit and not st.session_state.q_answered:
        if choice:
            st.session_state.q_answered = True
            st.session_state.total_q += 1
            if choice == q['ans']:
                st.session_state.score += 1
                st.balloons()
                st.success(f"✅ Correct! {q['expl']}")
            else:
                st.error(f"❌ Incorrect. The answer was {q['ans']}. \n\nReason: {q['expl']}")
        else:
            st.warning("Pick an answer first!")
            
    if st.session_state.q_answered:
        if st.button("Next Question ➡️"):
            st.session_state.current_q = random.choice(quiz_bank)
            st.session_state.q_answered = False
            st.rerun()

# --- TAB 4: LIBRARY ---
with tabs[3]:
    st.subheader("📚 Drug Library")
    for d in drug_database:
        with st.expander(d['class']):
            st.write(d)
