# Visualization Literacy Learning Tool 🧠📊

This web-based interactive tool was developed as part of the master's thesis *“Guide Me Through Visualizations”* at Freie Universität Berlin. It explores how different degrees of guidance can support non-experts in developing **visualization literacy (VL)** — the ability to understand, interpret, and critically evaluate data visualizations.

## 🧭 Purpose

The tool investigates the impact of **four degrees of user guidance** (no guidance, orienting, directing, and prescribing) in learning environments. It is based on:

- Human-centered design principles
- Modular learning materials inspired by cheat sheets
- Personalized recommendations based on CALVI assessment results

## 🎓 Thesis Abstract

> Visualization literacy (VL) — the ability to understand, interpret, and critically evaluate
data visualizations —is increasingly essential in today’s data-driven world. This thesis
investigates the impact of different degrees of guidance on the introduction of learning
materials designed to improve VL, particularly for non-experts. To explore this, four dis-
tinct interfaces of a modular, web-based learning tool were developed using the concept
of cheat sheets and following a human-centered design approach. Each interface incor-
porated one of four predefined levels of guidance: no guidance, orienting, directing, and
prescribing. The tool was integrated with the CALVI assessment, which evaluates indi-
viduals’ ability to identify and reason about misleading visualizations. An exploratory
between-subjects study (n = 20) was conducted with participants recruited via the online
platform Prolific, focusing on learning outcomes and user engagement across the differ-
ent guidance conditions. The interfaces employing orienting and prescribing guidance
demonstrated the most promising results. Although the findings are preliminary, they
provide valuable insights into the potential of system-guided support in VL education
and lay the groundwork for future research on guided learning systems.

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [LimeSurvey](https://www.limesurvey.org/) (for CALVI assessment integration)


## 🧩 Features

- Modular learning interface (Basics & Common Pitfalls)
- Personalized content via assessment token
- Visual feedback of user progress and score

## 📁 Repository Structure

Each folder includes an **identical structure** for modular learning content (e.g., `LearningContent/`, `Modules/`, `.streamlit/`). This redundancy was necessary to support the **independent deployment** of each interface in Streamlit Cloud. The **only file that differentiates each version is `Home.py`**, which contains the implementation logic specific to its degree of guidance.

## 🚀 Try the Interfaces

When clicking on the links below, you have access to the interfaces presenting the guidance based on a dummy assessment.
- No Guidance: Fully exploratory, no guidance provided. [Launch No Guidance🚀](https://visualizationliteracy1.streamlit.app/)
- Orienting Guidance: Visual cues to suggest relevant learning modules. [Launch Orienting🚀](https://visualizationliteracy2.streamlit.app/)
- Directing Guidance: Ranked module recommendations. [Launch Directing🚀](https://visualizationliteracy3.streamlit.app/) 
- Prescribing Guidance: Presents only recommended modules. [Launch Prescribing🚀](https://visualizationliteracy4.streamlit.app/)

## 📚 Academic References

- **CALVI Questionnaire**:  
  Lily W. Ge, Yuan Cui, and Matthew Kay. 2023. CALVI: Critical Thinking Assessment for Literacy in Visualizations. In Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems (CHI '23). Association for Computing Machinery, New York, NY, USA, Article 815, 1–18.
  DOI: [10.1145/3544548.3581406](https://doi.org/10.1145/3544548.3581406)


- **Visualization Cheat Sheets**:  
  Zezhong Wang, Lovisa Sundin, Dave Murray-Rust, and Benjamin Bach. 2020. Cheat Sheets for Data Visualization Techniques. In Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems (CHI '20). Association for Computing Machinery, New York, NY, USA, 1–13. 
  DOI: [10.1145/3313831.3376271](https://doi.org/10.1145/3313831.3376271)

- **Degrees of Guidance**:  
  D. Ceneda et al., "Characterizing Guidance in Visual Analytics," in IEEE Transactions on Visualization and Computer Graphics, vol. 23, no. 1, pp. 111-120, Jan. 2017.
  DOI: [10.1109/TVCG.2016.2598468](https://doi.org/10.1109/TVCG.2016.2598468)

These resources were instrumental in designing the learning materials, assessment mechanisms, and system-guided user interfaces.
