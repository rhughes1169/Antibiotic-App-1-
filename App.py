import streamlit as st
import random

# --- CONFIGURATION FOR IPAD ---
st.set_page_config(
    page_title="Antibiotic Master", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR TOUCH INTERFACE (IPAD) ---
st.markdown("""
<style>
    div.stButton > button {
        width: 100%;
        height: 3.5em;
        font-size: 18px !important;
        font-weight: bold;
        border-radius: 12px;
    }
    div.stRadio > div {
        gap: 15px;
        font-size: 18px;
    }
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: bold;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    h1, h2, h3 {
        font-family: 'Helvetica', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA SOURCE (Based on your PDF) ---
drug_database = [
    # --- PENICILLINS ---
    {
        "class": "Natural Penicillins (Group 1)",
        "drugs": "Penicillin G (IV/IM), Penicillin V (PO)",
        "spectrum": "Narrow: Gram-positive (Strep, Syphilis/Treponema, Meningococcus).",
        "adrs": "Hypersensitivity, Neurotoxicity (seizures), Renal failure[cite: 588].",
        "notes": "Susceptible to beta-lactamases (>90% S. aureus resistant). Pen G Benzathine is IM repository[cite: 468]."
    },
    {
        "class": "Anti-staphylococcal Penicillins (Group 2)",
        "drugs": "Methicillin, Nafcillin (IV), Oxacillin (IV), Dicloxacillin (PO) [cite: 511]",
        "spectrum": "MSSA (Methicillin-Sensitive Staph Aureus) & Strep.",
        "adrs": "Nafcillin: Phlebitis, Neutropenia. Methicillin: Interstitial Nephritis[cite: 523].",
        "notes": "Nafcillin is biliary excreted (liver), so no renal adjustment needed. NOT effective for MRSA[cite: 536]."
    },
    {
        "class": "Aminopenicillins (Group 3)",
        "drugs": "Ampicillin (IV), Amoxicillin (PO) [cite: 546]",
        "spectrum": "Gram-pos + some Gram-neg (H. flu, E. coli, Listeria).",
        "adrs": "Rash (non-allergic), Diarrhea.",
        "notes": "Often paired with beta-lactamase inhibitors (e.g., Amox/Clavulanate). Listeria requires Ampicillin[cite: 554]."
    },
    {
        "class": "Antipseudomonal Penicillins (Group 4)",
        "drugs": "Piperacillin, Ticarcillin [cite: 561]",
        "spectrum": "Pseudomonas aeruginosa, Klebsiella.",
        "adrs": "Bleeding risk (platelet dysfunction) at high doses[cite: 567].",
        "notes": "Piperacillin is the only one available in USA (as Pip/Tazo)[cite: 562]."
    },
    # --- CEPHALOSPORINS ---
    {
        "class": "1st Gen Cephalosporins",
        # Added Cefadroxil per request and PDF 
        "drugs": "Cefazolin (IV), Cephalexin (PO), Cefadroxil (PO)",
        "spectrum": "Gram-positive (MSSA, Strep) + PEcK (Proteus, E. coli, Klebsiella)[cite: 648].",
        "adrs": "Cross-reactivity with Penicillin allergy.",
        "notes": "Cefazolin is used for surgical prophylaxis. NOT for severe systemic infections (PO)[cite: 650]."
    },
    {
        "class": "2nd Gen Cephalosporins",
        "drugs": "Cefuroxime, Cefoxitin (IV), Cefotetan (IV) [cite: 676]",
        "spectrum": "Gram-pos + H. flu, Neisseria (HEN PEcK).",
        "adrs": "Cefotetan: Bleeding (anti-Vit K) & Disulfiram-like reaction with alcohol[cite: 765].",
        "notes": "Cefoxitin/Cefotetan have anaerobic activity (B. fragilis)[cite: 678]."
    },
    {
        "class": "3rd Gen Cephalosporins",
        # Added Cefotaxime and Cefpodoxime per request and PDF 
        "drugs": "Ceftriaxone (IV), Cefotaxime (IV), Ceftazidime (IV), Cefdinir (PO), Cefpodoxime (PO)",
        "spectrum": "Expanded Gram-neg. Crosses Blood-Brain Barrier (Meningitis).",
        "adrs": "Biliary sludging (Ceftriaxone).",
        "notes": "Ceftazidime is the ONLY 3rd gen active against Pseudomonas[cite: 697]. Ceftriaxone treats Gonorrhea[cite: 700]."
    },
    {
        "class": "4th Gen Cephalosporins",
        "drugs": "Cefepime (IV) [cite: 715]",
        "spectrum": "Broadest Ceph. Gram-pos + Gram-neg + Pseudomonas.",
        "adrs": "Encephalopathy (neurotoxicity)[cite: 726].",
        "notes": "Stable against beta-lactamases[cite: 718]."
    },
    {
        "class": "5th Gen Cephalosporins",
        "drugs": "Ceftaroline (IV) [cite: 743]",
        "spectrum": "Anti-MRSA.",
        "adrs": "Standard beta-lactam ADRs.",
        "notes": "Binds to PBP2a (mutated PBP in MRSA). Does NOT cover Pseudomonas[cite: 745]."
    },
    # --- OTHERS ---
    {
        "class": "Carbapenems",
        "drugs": "Imipenem/Cilastatin, Meropenem, Ertapenem [cite: 799]",
        "spectrum": "Very Broad: Gram+, Gram-, Anaerobes, Pseudomonas (except Ertapenem)[cite: 800].",
        "adrs": "Seizures (Imipenem risk > Meropenem)[cite: 808].",
        "notes": "Cilastatin inhibits renal dehydropeptidase to prevent Imipenem toxicity[cite: 807]."
    },
    {
        "class": "Monobactams",
        "drugs": "Aztreonam [cite: 772]",
        "spectrum": "Gram-negative AEROBES only (includes Pseudomonas)[cite: 773].",
        "adrs": "Low toxicity.",
        "notes": "Safe for patients with Penicillin anaphylaxis (no cross-reactivity)[cite: 796]."
    },
    {
        "class": "Glycopeptides",
        "drugs": "Vancomycin (IV/PO) [cite: 889]",
        "spectrum": "Gram-positive ONLY. MRSA. C. diff (PO only).",
        "adrs": "Red Man Syndrome (flushing), Ototoxicity, Nephrotoxicity[cite: 1023].",
        "notes": "Inhibits polymerization by binding D-Ala-D-Ala[cite: 964]. PO stays in gut[cite: 1001]."
    },
    {
        "class": "Lipopeptides",
        "drugs": "Daptomycin (IV) [cite: 1029]",
        "spectrum": "Gram-positive ONLY. MRSA, VRE.",
        "adrs": "Myopathy (monitor CPK weekly)[cite: 1066].",
        "notes": "Inactivated by pulmonary surfactant (Do NOT use for Pneumonia)[cite: 1172]. MOA: Depolarization."
    },
    {
        "class": "Others",
        "drugs": "Fosfomycin [cite: 1088]",
        "spectrum": "Gram+ and Gram-.",
        "adrs": "Diarrhea, vaginitis.",
        "notes": "Inhibits MurA (enolpyruvyl transferase)[cite: 1089]. Concentrates in bladder (UTIs)."
    }
]

# --- QUESTION BANK (MIXED ORDER) ---
# 1st Order: Fact Recall
# 2nd Order: Diagnosis -> Treatment
# 3rd Order: Management -> Complication -> Mechanism

quiz_bank = [
    # --- 1st ORDER QUESTIONS ---
    {
        "q": "Which drug inhibits cell wall synthesis by binding to the D-Ala-D-Ala terminus of the peptidoglycan precursor?",
        "options": ["Penicillin G", "Ceftriaxone", "Vancomycin", "Fosfomycin"],
        "answer": "Vancomycin",
        "expl": "Vancomycin binds D-Ala-D-Ala, preventing cross-linking. Beta-lactams bind PBPs. Fosfomycin inhibits MurA[cite: 964]."
    },
    {
        "q": "Which Cephalosporin generation is the only one with activity against MRSA?",
        "options": ["1st Gen (Cefazolin)", "3rd Gen (Ceftriaxone)", "4th Gen (Cefepime)", "5th Gen (Ceftaroline)"],
        "answer": "5th Gen (Ceftaroline)",
        "expl": "Ceftaroline is the only beta-lactam active against MRSA because it binds the mutated PBP2a[cite: 745]."
    },
    {
        "q": "What is the specific mechanism of action of Daptomycin?",
        "options": ["Binds PBP", "Binds D-Ala-D-Ala", "Inhibits Enolpyruvyl Transferase", "Causes Membrane Depolarization"],
        "answer": "Causes Membrane Depolarization",
        "expl": "Daptomycin inserts into the plasma membrane causing rapid depolarization and cell death[cite: 1031]."
    },
    # --- 2nd ORDER QUESTIONS ---
    {
        "q": "A patient has a confirmed Pseudomonas aeruginosa pneumonia. Which Penicillin class is appropriate?",
        "options": ["Natural Penicillin", "Aminopenicillin", "Antipseudomonal Penicillin", "Anti-staphylococcal Penicillin"],
        "answer": "Antipseudomonal Penicillin",
        "expl": "Only Piperacillin or Ticarcillin cover Pseudomonas. Aminopenicillins (Ampicillin) do NOT[cite: 561]."
    },
    {
        "q": "A pregnant patient has Syphilis (Treponema pallidum). What is the drug of choice?",
        "options": ["Penicillin G", "Vancomycin", "Aztreonam", "Cefepime"],
        "answer": "Penicillin G",
        "expl": "Penicillin G is the drug of choice for Syphilis[cite: 458]."
    },
    {
        "q": "A patient presents with a urinary tract infection. You prescribe Fosfomycin. Why is this drug effective for UTIs?",
        "options": ["It covers MRSA systemically", "It concentrates active drug in the bladder", "It is given IV only", "It treats Pyelonephritis only"],
        "answer": "It concentrates active drug in the bladder",
        "expl": "Fosfomycin is excreted by the kidneys and accumulates in the bladder, making it ideal for uncomplicated UTIs[cite: 1093]."
    },
    {
        "q": "A patient has meningitis. Which generation of Cephalosporins is most commonly used due to excellent CNS penetration?",
        "options": ["1st Gen", "2nd Gen", "3rd Gen", "1st Gen Oral"],
        "answer": "3rd Gen",
        "expl": "3rd Gen Cephalosporins (like Ceftriaxone) cross the blood-brain barrier well and are used for meningitis[cite: 695]."
    },
    # --- 3rd ORDER QUESTIONS ---
    {
        "q": "A patient is treated for a severe gram-negative infection with Imipenem. They suffer a seizure. What was the likely risk factor?",
        "options": ["Liver failure", "Renal failure/High dose", "Concomitant use of Penicillin", "Low dose therapy"],
        "answer": "Renal failure/High dose",
        "expl": "Seizures are a known ADR of Imipenem, especially in patients with renal impairment or high doses[cite: 808]."
    },
    {
        "q": "A patient with MRSA pneumonia is treated with an IV antibiotic and fails to improve. You realize the drug chosen is inactivated by pulmonary surfactant. Which drug was likely used?",
        "options": ["Vancomycin", "Linezolid", "Daptomycin", "Ceftaroline"],
        "answer": "Daptomycin",
        "expl": "Daptomycin is inactivated by surfactant, so it is contraindicated for pneumonia despite covering MRSA[cite: 1067]."
    },
    {
        "q": "A patient receives Cefotetan and later consumes alcohol, developing flushing and nausea. What is the mechanism?",
        "options": ["IgE Mediated Allergy", "Disulfiram-like reaction", "Red Man Syndrome", "Neurotoxicity"],
        "answer": "Disulfiram-like reaction",
        "expl": "Cefotetan (and Cefoxitin) can block alcohol oxidation, leading to a Disulfiram-like reaction[cite: 766]."
    },
    {
        "q": "A patient on Nafcillin develops neutropenia. What is the route of elimination for this specific drug?",
        "options": ["Renal Filtration", "Biliary Excretion", "Lung Exhalation", "Sweat"],
        "answer": "Biliary Excretion",
        "expl": "Nafcillin is unique among penicillins as it is primarily eliminated via biliary excretion (liver), not kidneys[cite: 536]."
    },
    {
        "q": "A patient develops 'Red Man Syndrome' during an infusion. This reaction is mediated by:",
        "options": ["IgE Antibodies", "T-Cell activation", "Direct Histamine Release", "Renal toxicity"],
        "answer": "Direct Histamine Release",
        "expl": "This is a histamine-mediated flushing syndrome caused by rapid infusion of Vancomycin, NOT an IgE allergy[cite: 1023]."
    },
     {
        "q": "You need to treat a Pseudomonas infection but the patient has a severe anaphylactic reaction to Penicillins. Which drug is safest?",
        "options": ["Cefepime", "Imipenem", "Aztreonam", "Piperacillin"],
        "answer": "Aztreonam",
        "expl": "Aztreonam (Monobactam) has little to no cross-reactivity with Penicillins and is safe for allergic patients[cite: 796]."
    },
    {
        "q": "Which combination represents a Penicillin paired with a Beta-Lactamase Inhibitor?",
        "options": ["Ampicillin + Sulbactam", "Amoxicillin + Azithromycin", "Piperacillin + Cilastatin", "Penicillin G + Clavulanate"],
        "answer": "Ampicillin + Sulbactam",
        "expl": "Ampicillin is often paired with Sulbactam (Unasyn) to restore activity against beta-lactamase producing organisms[cite: 548]."
    }
]

# --- APP HEADER ---
st.title("💊 Cell Wall Master")
st.caption("Interactive Study Companion | Updated with PDF Source Material")

# --- TABS (Navigation) ---
tab1, tab2, tab3 = st.tabs(["⚡ Flashcards", "📚 Library", "🧠 Quiz Bank"])

# --- TAB 1: FLASHCARDS (Touch Optimized) ---
with tab1:
    st.markdown("### Active Recall")
    
    if 'flashcard_idx' not in st.session_state:
        st.session_state.flashcard_idx = random.randint(0, len(drug_database)-1)
        st.session_state.reveal_card = False

    current_card = drug_database[st.session_state.flashcard_idx]

    with st.container(border=True):
        st.markdown(f"**Drug Class:**")
        st.header(current_card['class'])
        st.divider()
        
        if st.session_state.reveal_card:
            st.success(f"**💊 Drugs:** {current_card['drugs']}")
            st.info(f"**🦠 Spectrum:** {current_card['spectrum']}")
            st.warning(f"**⚠️ ADRs:** {current_card['adrs']}")
            st.markdown(f"**📝 Note:** {current_card['notes']}")
        else:
            st.markdown("*Tap 'Reveal' to see Drugs, Spectrum, and ADRs*")
            st.markdown("<br>" * 3, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("👁️ REVEAL", use_container_width=True):
            st.session_state.reveal_card = True
            st.rerun()
    with col_b:
        if st.button("➡️ NEXT CARD", type="primary", use_container_width=True):
            st.session_state.flashcard_idx = random.randint(0, len(drug_database)-1)
            st.session_state.reveal_card = False
            st.rerun()

# --- TAB 2: LIBRARY ---
with tab2:
    st.markdown("### Drug Class Reference")
    st.markdown("Tap to expand details.")
    
    for item in drug_database:
        with st.expander(item['class']):
            st.markdown(f"**Drugs:** {item['drugs']}")
            st.markdown(f"**Spectrum:** {item['spectrum']}")
            st.markdown(f"**ADRs:** {item['adrs']}")
            st.caption(f"*{item['notes']}*")

# --- TAB 3: QUIZ BANK (RANDOMIZED) ---
with tab3:
    st.markdown("### Mixed Order Question Bank")
    st.caption("Randomly selects 1st, 2nd, and 3rd order questions.")

    # Initialize session state for the quiz
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = random.randint(0, len(quiz_bank)-1)
        st.session_state.quiz_submitted = False
        st.session_state.selected_opt = None

    q = quiz_bank[st.session_state.quiz_index]

    st.progress((st.session_state.quiz_index + 1) / len(quiz_bank), text=f"Question Pool ID: {st.session_state.quiz_index}")

    st.subheader(q['q'])
    
    # Radio button for selection
    # We use a placeholder key that changes when we hit 'next' to reset the selection
    choice = st.radio(
        "Select your answer:", 
        q['options'], 
        index=None,
        key=f"radio_{st.session_state.quiz_index}" 
    )

    # Check Answer Button
    if st.button("Check Answer", type="primary", use_container_width=True):
        if choice == q['answer']:
            st.success(f"✅ Correct! \n\n**Explanation:** {q['expl']}")
        elif choice is None:
            st.warning("Please select an answer.")
        else:
            st.error(f"❌ Incorrect. \n\nThe correct answer is **{q['answer']}**.\n\n**Explanation:** {q['expl']}")

    st.divider()

    # Next Question Button
    if st.button("➡️ New Random Question", use_container_width=True):
        st.session_state.quiz_index = random.randint(0, len(quiz_bank)-1)
        st.rerun()
        import streamlit as st
import random
import graphviz

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Antibiotic Master Visual", 
    layout="wide", # Wide layout is better for diagrams
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

# [cite_start]--- DATA SOURCE [cite: 412, 626, 771, 888, 1029] ---
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
    {"q": "Target: D-Ala-D-Ala. [cite_start]Drug?", "opt": ["Vancomycin", "Penicillin", "Daptomycin"], "ans": "Vancomycin", "expl": "Vancomycin binds the D-Ala-D-Ala tail[cite: 987]."},
    {"q": "Patient has Pseudomonas. Penicillin allergy (Anaphylaxis). [cite_start]Safe choice?", "opt": ["Piperacillin", "Cefepime", "Aztreonam"], "ans": "Aztreonam", "expl": "Monobactams have no cross-reactivity[cite: 796]."},
    [cite_start]{"q": "Which drug is inactivated by Lung Surfactant?", "opt": ["Daptomycin", "Linezolid", "Ceftaroline"], "ans": "Daptomycin", "expl": "Daptomycin cannot treat pneumonia[cite: 1172]."},
    [cite_start]{"q": "Drug causing 'Red Man Syndrome'?", "opt": ["Vancomycin", "Nafcillin", "Cefotetan"], "ans": "Vancomycin", "expl": "Histamine release due to rapid infusion[cite: 1023]."},
    [cite_start]{"q": "Only Cephalosporin active against MRSA?", "opt": ["Ceftaroline", "Cefepime", "Ceftriaxone"], "ans": "Ceftaroline", "expl": "5th Gen Ceftaroline binds PBP2a[cite: 744]."},
    [cite_start]{"q": "3rd Gen Cephalosporin that covers Pseudomonas?", "opt": ["Ceftazidime", "Ceftriaxone", "Cefotaxime"], "ans": "Ceftazidime", "expl": "Ceftazidime is the specific 3rd gen for Pseudomonas[cite: 697]."},
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
        # [cite_start]Graphviz code to visualize MOA [cite: 280-287, 1029, 1089]
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
        # [cite_start]Graphviz for Cephalosporins [cite: 626-759]
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
