QA_SET=[
    {
        'qa_id':'institution_101',
        'question':'What did the Treaty of Lisbon rename the Treaty establishing the European Community as?',
        'question_type':'extractive',
        'topic_category':'institutions',
        'gold_answer':'It was renamed the Treaty on the Functioning of the European Union (TFEU), and the term Community was replaced by Union throughout the text.',
        'gold_sources':[{'source':'en-chapter-1.pdf',
                        'page':21,
                        'text_span':"renamed the 'Treaty on the Functioning of the European Union' (TFEU) and the term 'Community' is replaced by 'Union' throughout the text"}],
        'difficulty':'easy',
        'notes':'Single-fact lookup from section 1.1.5, opening paragraph of CONTENT'
    },

    {
        'qa_id':'legislative_procedure_101',
        'question': 'Under the principle of subsidiarity, when is it preferable for the EU to act rather than the Member States?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'When the objectives of an action cannot be sufficiently achieved by the Member States alone, but can be better achieved at Union level because of the scale or effects of the proposed action, in areas where the EU does not have exclusive competence.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 34,
                          'text_span': 'authorises intervention by the Union when the objectives'}],
        'difficulty': 'medium',
        'notes': 'Core EPSO-relevant legal concept (Article 5(3) TEU). Section 1.2.2.'
    },

    {   
        'qa_id':'legislative_procedure_102',
        'question':'Which treaty gave the European Parliament an equal say with the Council over the entire EU budget?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'The Treaty of Lisbon, which entered into force in 2009.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 53,
                          'text_span': 'gave Parliament an equal say with the Council'}],
        'difficulty': 'easy',
        'notes': 'Section 1.2.5, summary box. Classified under legislative_procedure rather than  budget since the question is about the procedural/decision-making change, not a budget figure.'
    },

    {   
        'qa_id': 'institutions_102',
        'question': "Since which treaty has Parliament 's assent been required for treaties admitting a new Member State?",
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'Since the Single European Act (SEA).',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 63,
                          'text_span': 'all treaties marking the accession of a new'}],
        'difficulty': 'medium',
        'notes': "Section 1.3.2, under 'Constitutional-type powers and ratification powers'."
    },

    {   
        'qa_id': 'institutions_103',
        'question': 'What is the key institutional difference between the European Council and the Council of the European Union?',
        'question_type': 'synthesis',
        'topic_category': 'institutions',
        'gold_answer': 'The European Council brings together the heads of state or government to provide political direction and set priorities for the EU, and was made a full EU institution by the Treaty of Lisbon. The Council of the European Union is the body that, together with Parliament, adopts EU legislation (regulations and directives). They are formally separate institutions, even though they share Section II of the EU budget.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 87,
                          'text_span': 'provide the Union with the necessary impetus'},
                            {   'source': 'en-chapter-1.pdf',
                                'page': 94,
                                'text_span': 'adopts EU legislation in the form of regulations'}],
        'difficulty': 'hard',
        'notes': "Deliberately mirrors the classic EPSO 'Council vs European Council' distractor pattern flagged earlier. Requires combining sections 1.3.6 and 1.3.7 -- not answerable from a single chunk, so this item's primary metric should be RAGAS Context Precision/Faithfulness rather than single-chunk Recall@k."
    },

    {   
        'qa_id': 'institutions_104',
        'question': 'How many advocates-general assist the Court of Justice of the European Union?',
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': '11 advocates-general.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 105,
                          'text_span': 'assisted by 11 advocates-general'}],
        'difficulty':'easy',
        'notes':'Section 1.3.9, Composition and Statute. Numeric answer -- also a good candidate for the optional MCQ end-task metric later.'
    },

    {   
        'qa_id': 'internal_market_101',
        'question': 'What four freedoms does the EU internal market guarantee?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'Free movement of goods, services, capital and persons.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 5,
                          'text_span': 'free movement of goods, services, capital and persons'}],
        'difficulty': 'easy',
        'notes': 'Section 2.1.1, opening summary box.'
    },

    {   
        'qa_id': 'internal_market_102',
        'question': 'Which CJEU rulings in the 1970s introduced the principle of mutual recognition into the internal market?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer':'The Dassonville and Cassis de Dijon rulings, which held that import restrictions with an effect equivalent to quantitative restrictions were unlawful.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 5,
                          'text_span': 'Dassonville (Case 8-74) and the Cassis de Dijon'}],
        'difficulty': 'hard',
        'notes': 'Section 2.1.1, part B. Same source page as internal_market_101 but a different paragraph -- tests retrieval precision, not just page-level recall.'
    },
    
    {   
        'qa_id': 'internal_market_103',
        'question': 'Which EU agency serves as the dedicated agency for the free movement of workers, including posted workers?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'The European Labour Authority.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 26,
                          'text_span': 'European Labour Authority serves as a dedicated agency'}],
        'difficulty': 'easy',
        'notes': 'Section 2.1.5, summary box.'
    },

    {   
        'qa_id': 'internal_market_104',
        'question': "What are the EU 's five main energy policy aims set out under the 2015 Energy Union strategy?",
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'Diversifying energy sources for security through EU solidarity; a fully integrated internal energy market; improving energy efficiency and cutting import dependence; decarbonising the economy in line with the Paris Agreement; and promoting research in low-carbon and clean energy technologies.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 203,
                          'text_span': "five main aims of the EU's energy policy"}],
        'difficulty': 'medium',
        'notes': 'Section 2.4.7. Multi-part enumerated answer, good candidate for testing whether a retrieved chunk captures the full list or only part of it.'
    },

    {   
        'qa_id': 'economic_governance_101',
        'question': 'What is the difference between the Economic and Monetary Union (EMU) itself and the institutions of the EMU?',
        'question_type': 'synthesis',
        'topic_category': 'economic_governance',
        'gold_answer': 'EMU is the broader framework of progressive economic integration built on the single market, centred on the euro and coordinated fiscal/monetary policy, with no single central economic government. The institutions of the EMU are the specific bodies that operationalise it: the European Central Bank, the European System of Central Banks, the Economic and Financial Committee, the Eurogroup, and Ecofin.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 275,
                          'text_span': 'no central economic government'},
                        {'source': 'en-chapter-2.pdf',
                         'page': 281,
                         'text_span': 'these institutions are: the European Central Bank'}],
        'difficulty': 'hard',
        'notes': 'Requires combining sections 2.6.1 and 2.6.2. Primary metric should be RAGAS-based, not single-chunk Recall@k, for the same reason as institutions_103.'
    },

    {   
        'qa_id': 'economic_governance_102',
        'question': 'Which regulation governs the assessment of mergers and takeovers with an EU dimension?',
        'question_type': 'extractive',
        'topic_category': 'economic_governance',
        'gold_answer': 'The Merger Regulation, Council Regulation (EC) No 139/2004.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 329,
                           'text_span': 'Merger Regulation (Council Regulation (EC) No 139/2004)'}],
        'difficulty': 'medium',
        'notes': 'Section 2.6.12, Legal Basis.'
    },

    {   
        'qa_id': 'budget_101',
        'question': 'Which treaty introduced territorial cohesion as a third dimension of EU cohesion '
                    'policy, alongside economic and social cohesion?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'The Treaty of Lisbon, in 2008.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 4,
                          'text_span': 'introduced a third dimension of EU cohesion'}],
        'difficulty': 'medium',
        'notes': 'Section 3.1.1, Context.'
    },

    {   
        'qa_id': 'budget_102',
        'question': "What GDP-per-capita threshold defines a 'less-developed region' eligible for the top tier of ERDF support?",
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'Regions whose GDP per capita is below 75% of the EU average.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 7,
                          'text_span': 'GDP per capita is below 75% of the'}],
        'difficulty': 'medium',
        'notes': 'Section 3.1.2, Objectives. Numeric threshold, good MCQ-distractor candidate (75% vs the 90% threshold used for Cohesion Fund eligibility, see budget_103).'
    },

    {   
        'qa_id': 'budget_103',
        'question': 'How does the Cohesion Fund differ from the EU Solidarity Fund in purpose and eligibility?',
        'question_type': 'synthesis',
        'topic_category': 'budget',
        'gold_answer': 'The Cohesion Fund is an ongoing structural investment instrument that funds environmental and transport infrastructure projects, restricted to Member States whose gross national income per capita is below 90% of the EU average. The Solidarity Fund is a reactive emergency-support instrument that provides grants to any Member State or accession candidate affected by a major natural disaster or public health emergency, regardless of income level.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 10,
                          'text_span': 'gross national income per capita is less than'},
                          {'source': 'en-chapter-3.pdf',
                           'page': 1,
                           'text_span': 'provide financial support to a Member State'}],
        'difficulty': 'hard',
        'notes': "Deliberately mirrors the EPSO near-identical-fund-names distractor pattern (compare institutions_103 's Council/European Council pair). Requires combining sections 3.1.3 and 3.1.4."
    },

    {   
        'qa_id': 'budget_104',
        'question': 'In 2007, which two funds replaced the European Agricultural Guidance and Guarantee Fund (EAGGF) for financing the CAP?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'The European Agricultural Guarantee Fund (EAGF) and the European Agricultural Fund for Rural Development (EAFRD).',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 43,
                          'text_span': 'European Agricultural Guarantee Fund (EAGF) and the'}],
        'difficulty': 'medium',
        'notes': 'Section 3.2.2, summary box. Classified as budget (financing mechanism) rather than sectoral_policy, parallel to how ERDF/Cohesion Fund items are classified.'
    },
    
    {   
        'qa_id': 'sectoral_policy_101',
        'question': 'Which decision-making procedure did the Treaty of Lisbon establish for the Common Agricultural Policy, replacing the consultation procedure?',
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': "Codecision, recognised as the 'ordinary legislative procedure' for the CAP.",
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 38,
                          'text_span': "recognised codecision as the 'ordinary legislative procedure'"}],
        'difficulty': 'medium',
        'notes': 'Section 3.2.1, summary box. Bridges sectoral_policy and legislative_procedure flagged in case you would rather reclassify.'
    },

    {   
        'qa_id': 'sectoral_policy_102',
        'question': 'Roughly what share of total EU greenhouse gas emissions does the transport sector account for?',
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'Roughly a quarter of total EU greenhouse gas emissions from human activity.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 136,
                          'text_span': 'transport sector accounts for roughly a quarter'}],
        'difficulty': 'easy',
        'notes': 'Section 3.4.1, Legal Basis and Objectives.'
    },

    {
        'qa_id': 'institutions_105',
        'question': 'What was the European Parliament originally called when it first met in Strasbourg in 1958, and when did it adopt its current name?',
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'It first met as the "European Parliamentary Assembly" on 19 March 1958, and changed its name to the "European Parliament" on 30 March 1962.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 59,
                          'text_span': "met for the first time in Strasbourg on 19 March 1958 as the"}],
        'difficulty': 'medium',
        'notes': 'Section 1.3.1, "Three communities, one assembly".'
    },

    {
        'qa_id': 'institutions_106',
        'question': 'When did the first direct elections to the European Parliament take place?',
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'On 7 and 10 June 1979.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 59,
                          'text_span': 'act entered into force on July 1978, and the first elections took place on 7 and 10 June 1979'}],
        'difficulty': 'easy',
        'notes': 'Section 1.3.1, "From appointed assembly to elected parliament".'
    },

    {
        'qa_id': 'institutions_107',
        'question': 'What are the two courts that together make up the Court of Justice of the European Union?',
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'The Court of Justice proper and the General Court.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 111,
                          'text_span': 'consists of two courts, the Court of Justice'}],
        'difficulty': 'easy',
        'notes': 'Section 1.3.10, opening description.'
    },

    {
        'qa_id': 'institutions_108',
        'question': 'Under Article 260 TFEU, what can the Court of Justice do if a Member State fails to comply with a judgment finding it in breach of EU law?',
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'It may impose a financial penalty on the Member State, consisting of a fixed lump sum and/or a periodic penalty payment, with the amount set by the Court based on a Commission proposal.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 111,
                          'text_span': 'it may impose on it a financial penalty (a fixed lump sum and/or a periodic penalty payment)'}],
        'difficulty': 'medium',
        'notes': 'Section 1.3.10, proceedings against a Member State for failure to fulfil an obligation.'
    },

    {
        'qa_id': 'institutions_109',
        'question': "What is the European Investment Bank 's relationship to the European Investment Fund?",
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'The EIB is the majority shareholder in the European Investment Fund (EIF), and together the two organisations form the EIB Group.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 136,
                          'text_span': 'The EIB is the majority shareholder in the European Investment Fund (EIF), and the two organisations together make up the EIB Group'}],
        'difficulty': 'easy',
        'notes': 'Section 1.3.15, opening description.'
    },

    {
        'qa_id': 'institutions_110',
        'question': 'What are the six priority areas of European Investment Bank activity?',
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'Climate and environment; development; innovation and skills; small businesses; infrastructure; and cohesion.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 136,
                          'text_span': 'EIB activities focus on six priority areas: climate and environment; development; innovation and skills; small businesses; infrastructure; and cohesion'}],
        'difficulty': 'medium',
        'notes': 'Section 1.3.15, Objectives.'
    },

    {
        'qa_id': 'institutions_111',
        'question': 'What number of Commissioners did the European Council decide on in 2009 for the composition of the Commission, and how did this compare to what the Treaty of Lisbon had originally stipulated?',
        'question_type': 'synthesis',
        'topic_category': 'institutions',
        'gold_answer': 'The Treaty of Lisbon had originally stipulated that from November 2014 the Commission would have a membership equal to two thirds of the number of Member States, while giving the European Council flexibility to change this. In 2009 the European Council decided the Commission would instead keep one Commissioner per Member State.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 99,
                          'text_span': 'was to be equivalent to two thirds of the number of Member States'},
                          {'source': 'en-chapter-1.pdf',
                           'page': 99,
                           'text_span': 'the Commission would continue to consist of a number of members equal to the number of Member States'}],
        'difficulty': 'hard',
        'notes': 'Section 1.3.8, Composition and legal status. Requires combining the original Lisbon provision with the 2009 European Council decision, both on the same page but different sentences.'
    },

    {
        'qa_id': 'institutions_112',
        'question': 'Since 2014, what additional task has the European Central Bank been responsible for beyond monetary policy?',
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'Prudential supervision of credit institutions, under the Single Supervisory Mechanism.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 117,
                          'text_span': 'the ECB has been responsible for tasks relating to the prudential supervision of credit institutions under the Single Supervisory Mechanism'}],
        'difficulty': 'medium',
        'notes': 'Section 1.3.11, opening description.'
    },

    {
        'qa_id': 'institutions_113',
        'question': 'What is the difference between the European System of Central Banks (ESCB) and the Eurosystem?',
        'question_type': 'extractive',
        'topic_category': 'institutions',
        'gold_answer': 'The ESCB comprises the ECB and the national central banks of all EU Member States, including those that have not adopted the euro, while the Eurosystem comprises only the ECB and the national central banks of Member States that have adopted the euro.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 117,
                          'text_span': 'The Eurosystem, meanwhile, comprises the ECB and the national central banks of only those Member States that have adopted the euro'}],
        'difficulty': 'medium',
        'notes': 'Section 1.3.11, Monetary function. Single-page, single-paragraph distinction.'
    },

    {
        'qa_id': 'legislative_procedure_103',
        'question': 'Into what three types does EU law divide its legal order?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'Primary legislation (the Treaties and general legal principles), secondary legislation (based on the Treaties), and supplementary law.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 28,
                          'text_span': 'divided into primary legislation (the Treaties and general legal principles), secondary legislation (based on the Treaties) and supplementary law'}],
        'difficulty': 'easy',
        'notes': 'Section 1.2.1, opening paragraph.'
    },

    {
        'qa_id': 'legislative_procedure_104',
        'question': 'Which two landmark CJEU cases established the doctrines of direct effect and primacy of EU law?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'Van Gend en Loos v Nederlandse Administratie der Belastingen, and Costa v ENEL.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 28,
                          'text_span': 'landmark cases van Gend en Loos v Nederlandse Administratie der Belastingen  and Costa v ENEL'}],
        'difficulty': 'medium',
        'notes': 'Section 1.2.1, hierarchy of Union law paragraph.'
    },

    {
        'qa_id': 'legislative_procedure_105',
        'question': 'According to Article 288 TFEU, what are the five kinds of legal acts EU institutions may adopt?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'Regulations, directives, decisions, recommendations and opinions.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 29,
                          'text_span': 'They are regulations, directives, decisions, recommendations and opinions'}],
        'difficulty': 'easy',
        'notes': 'Section 1.2.1, secondary legislation, general points.'
    },

    {
        'qa_id': 'legislative_procedure_106',
        'question': 'What three categories does the TFEU divide Union competences into?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'Exclusive competences, shared competences, and supporting competences.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 29,
                          'text_span': 'dividing them into three categories: exclusive competences (Article 3), shared competences (Article 4) and supporting competences (Article 6)'}],
        'difficulty': 'medium',
        'notes': 'Section 1.2.1, secondary legislation, general points.'
    },

    {
        'qa_id': 'legislative_procedure_107',
        'question': 'What was the ordinary legislative procedure previously known as, before the Treaty of Lisbon renamed it?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'The codecision procedure.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 41,
                          'text_span': 'the ordinary legislative procedure, formerly called the codecision procedure'}],
        'difficulty': 'easy',
        'notes': 'Section 1.2.3, Ordinary legislative procedure, scope.'
    },

    {
        'qa_id': 'legislative_procedure_108',
        'question': 'By what majority does Parliament adopt its position at first reading under the ordinary legislative procedure, and by what majority does the Council adopt its position?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'Parliament adopts its position by a simple majority, and the Council adopts its position by qualified majority voting (QMV).',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 42,
                          'text_span': 'Parliament adopts its position by a simple majority'}],
        'difficulty': 'medium',
        'notes': 'Section 1.2.3, Procedure, steps b and c.'
    },

    {
        'qa_id': 'legislative_procedure_109',
        'question': 'Which fields use intergovernmental decision-making procedures rather than the ordinary legislative procedure?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'The Common Foreign and Security Policy (CFSP), as well as several other fields such as enhanced cooperation, certain appointments, and treaty revision.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 47,
                          'text_span': 'In the Common Foreign and Security Policy (CFSP), as well as in several other fields such as enhanced cooperation, certain appointments and treaty revision'}],
        'difficulty': 'medium',
        'notes': 'Section 1.2.4, opening description.'
    },

    {
        'qa_id': 'legislative_procedure_110',
        'question': 'Under the Treaty amendment procedure of Article 48 TEU, who can propose an amendment to the Treaties?',
        'question_type': 'extractive',
        'topic_category': 'legislative_procedure',
        'gold_answer': 'Any Member State, Parliament, or the Commission.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 47,
                          'text_span': 'Proposal: any Member State, Parliament or the Commission'}],
        'difficulty': 'easy',
        'notes': 'Section 1.2.4, Procedure for amendment of the Treaties.'
    },

    {
        'qa_id': 'legislative_procedure_111',
        'question': "How did Parliament 's role in EU decision-making change from the Treaty of Rome through to the Treaty of Nice?",
        'question_type': 'synthesis',
        'topic_category': 'legislative_procedure',
        'gold_answer': "Under the Treaty of Rome, Parliament had only a consultative power. Its role then grew progressively: in the budgetary domain through the 1970 and 1975 reforms, in the legislative domain through the Single European Act and later the Treaty of Maastricht (which introduced codecision), and further under the Treaty of Amsterdam, which simplified and extended codecision and strengthened Parliament's role in appointing the Commission. The Treaty of Nice then considerably increased Parliament's powers further, extending codecision to almost all areas of qualified-majority Council decisions.",
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 41,
                          'text_span': 'It gave Parliament a consultative power'},
                          {'source': 'en-chapter-1.pdf',
                           'page': 41,
                           'text_span': 'the Treaty of Nice considerably increased Parliament powers'}],
        'difficulty': 'hard',
        'notes': 'Section 1.2.3, History paragraph. Requires tracing the progression across several treaties described in one continuous paragraph.'
    },

    {
        'qa_id': 'budget_105',
        'question': 'What percentage of EU gross national income (GNI) is the current ceiling on own resources that can be called on per year?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'A maximum of 1.4% of EU gross national income (GNI).',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 148,
                          'text_span': 'sources that can be called on per year is currently limited to a maximum of 1.4% of EU gross national income (GNI)'}],
        'difficulty': 'medium',
        'notes': 'Section 1.4.1, How it works.'
    },

    {
        'qa_id': 'budget_106',
        'question': "What are the three main 'traditional' categories that made up the EU's traditional own resources?",
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'Customs duties, agricultural duties, and sugar levies.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 149,
                          'text_span': 'These consist of customs duties, agricultural duties and sugar levies collected since 1970'}],
        'difficulty': 'easy',
        'notes': 'Section 1.4.1, Revenue composition, "Traditional" own resources.'
    },

    {
        'qa_id': 'budget_107',
        'question': 'What did the Treaty of Lisbon change about the legal nature of the multiannual financial framework (MFF)?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'It transformed the MFF from an interinstitutional agreement into a (Council) regulation.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 158,
                          'text_span': 'The Treaty of Lisbon transformed the MFF from an interinstitutional agreement into a regulation'}],
        'difficulty': 'medium',
        'notes': 'Section 1.4.3, opening description.'
    },

    {
        'qa_id': 'budget_108',
        'question': 'How large was the NextGenerationEU recovery instrument proposed by the Commission in response to COVID-19?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'EUR 750 billion, in 2018 prices.',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 158,
                          'text_span': 'the setting up of a recovery instrument worth EUR 750 billion (in 2018 prices)'}],
        'difficulty': 'medium',
        'notes': 'Section 1.4.3, Background.'
    },

    {
        'qa_id': 'budget_109',
        'question': 'Into what three categories of regions are ERDF "Investment for growth and jobs" resources allocated, based on GDP per capita?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'More-developed regions (GDP per capita above 100% of the EU average), transition regions (between 75% and 100%), and less-developed regions (below 75%).',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 7,
                          'text_span': 'Less-developed regions whose GDP per capita is below 75% of the EU average'}],
        'difficulty': 'medium',
        'notes': 'Section 3.1.2, Objectives. Same page as budget_102 (already in the pilot set) but a different, broader fact -- tests whether retrieval favors the specific 75% figure over the full three-tier breakdown.'
    },

    {
        'qa_id': 'budget_110',
        'question': 'Roughly how much of the EUR 392 billion allocated to cohesion policy for 2021-2027 went to the ERDF specifically?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'Around EUR 226 billion.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 8,
                          'text_span': 'Around EUR 226 billion was allocated to the ERDF'}],
        'difficulty': 'medium',
        'notes': 'Section 3.1.2, Budget and financial rules.'
    },

    {
        'qa_id': 'budget_111',
        'question': 'What are the three pillars of the Just Transition Mechanism?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': 'The Just Transition Fund; a dedicated scheme under the InvestEU programme; and a public sector loan facility provided by the European Investment Bank.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 31,
                          'text_span': 'The Just Transition Fund; A dedicated scheme under the InvestEU programme; A public sector loan facility provided by the European Investment Bank'}],
        'difficulty': 'medium',
        'notes': 'Section 3.1.10, Context.'
    },

    {
        'qa_id': 'budget_112',
        'question': 'What long-term climate goal is the Just Transition Fund designed to help implement?',
        'question_type': 'extractive',
        'topic_category': 'budget',
        'gold_answer': "The European Green Deal 's goal of making the EU climate-neutral by 2050.",
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 31,
                          'text_span': 'implementation of the European Green Deal, which aims to make the EU climate-neutral by 2050'}],
        'difficulty': 'easy',
        'notes': 'Section 3.1.10, opening description.'
    },

    {
        'qa_id': 'budget_113',
        'question': 'How does the funding mechanism of the Cohesion Fund differ from that of the Just Transition Fund and the InvestEU scheme?',
        'question_type': 'synthesis',
        'topic_category': 'budget',
        'gold_answer': 'The Cohesion Fund and the Just Transition Fund primarily provide grants, restricted by eligibility criteria such as income thresholds or exposure to the climate transition. The InvestEU pillar, by contrast, works by crowding in private investment rather than providing direct grants, and the European Investment Bank pillar leverages public financing.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 31,
                          'text_span': 'The Just Transition Fund primarily provides grants. The dedicated transition scheme under InvestEU crowds in private investments'}],
        'difficulty': 'hard',
        'notes': 'Section 3.1.10, funding mechanism paragraph. Requires distinguishing grant-based vs investment-crowding-in mechanisms described together in one paragraph.'
    },

    {
        'qa_id': 'internal_market_105',
        'question': 'By what date was the elimination of customs duties and quantitative restrictions between Member States accomplished?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'By 1 July 1968.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 11,
                          'text_span': 'was accomplished by 1 July 1968'}],
        'difficulty': 'easy',
        'notes': 'Section 2.1.2, Achievements.'
    },

    {
        'qa_id': 'internal_market_106',
        'question': "What did the Court of Justice's 'Dassonville' judgment establish about national trading rules?",
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'That all trading rules enacted by Member States which are capable of hindering intra-Community trade, directly or indirectly, actually or potentially, are to be considered measures having an effect equivalent to quantitative restrictions.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 12,
                          'text_span': 'all trading rules enacted by Member States which are capable of hindering, directly or indirectly, actually or potentially, intra-Community trade were to be considered as measures having an effect equivalent to quantitative restrictions'}],
        'difficulty': 'hard',
        'notes': 'Section 2.1.2, part B, prohibition of measures equivalent to quantitative restrictions.'
    },

    {
        'qa_id': 'internal_market_107',
        'question': 'When was the first EU research framework programme established, and how long did it run for?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'It was established in 1983, for a four-year period.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 193,
                          'text_span': 'The first framework programme (FP) was established in 1983, for a four-year period'}],
        'difficulty': 'easy',
        'notes': 'Section 2.4.5, Achievements, Research framework programmes.'
    },

    {
        'qa_id': 'internal_market_108',
        'question': 'What is Horizon Europe, and what is its budget?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': "Horizon Europe is the EU 's current research and innovation programme (the ninth framework programme), launched in 2021 for the 2021-2027 period, with a budget of EUR 95.5 billion.",
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 193,
                          'text_span': 'Horizon Europe, the ninth FP, is the biggest and most ambitious, with a budget of EUR 95.5 billion'}],
        'difficulty': 'medium',
        'notes': 'Section 2.4.5, Achievements, Research framework programmes.'
    },

    {
        'qa_id': 'internal_market_109',
        'question': 'What legal instrument, adopted in 2008, strengthened the free movement of goods, EU market surveillance, and the CE mark?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'The New Legislative Framework.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 11,
                          'text_span': 'The adoption of the New Legislative Framework in 2008 strengthened the free movement of goods, the EU market surveillance system and the CE (European conformity) mark'}],
        'difficulty': 'medium',
        'notes': 'Section 2.1.2, opening description.'
    },

    {
        'qa_id': 'internal_market_110',
        'question': 'Under Article 28 of the TFEU, what right underpins the free movement of goods?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'The right to the free movement of goods originating in Member States, and of goods from third countries which are in free circulation in the Member States.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 11,
                          'text_span': 'The right to the free movement of goods originating in Member States, and of goods from third countries which are in free circulation in the Member States, is one of the fundamental principles of the Treaty'}],
        'difficulty': 'medium',
        'notes': 'Section 2.1.2, Objectives.'
    },

    {
        'qa_id': 'internal_market_111',
        'question': 'What was the original scope of the common market envisioned under the EEC Treaty (Treaty of Rome), before it evolved into the internal market?',
        'question_type': 'synthesis',
        'topic_category': 'internal_market',
        'gold_answer': 'It was originally framed as part of a customs union between Member States, involving the abolition of customs duties, quantitative restrictions and equivalent measures, plus a common external tariff. Later the emphasis shifted to eliminating remaining obstacles to free movement of goods more broadly, with the goal of creating the internal market.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 11,
                          'text_span': 'the free movement of goods was seen as part of a customs union between the Member States'},
                          {'source': 'en-chapter-2.pdf',
                           'page': 11,
                           'text_span': 'Later on, the emphasis was placed on eliminating all remaining obstacles to the free movement of goods, with a view to creating the internal market'}],
        'difficulty': 'hard',
        'notes': 'Section 2.1.2, Objectives -- traces the shift from customs union framing to internal market framing across two sentences on the same page.'
    },

    {
        'qa_id': 'internal_market_112',
        'question': 'What sensitive areas caused the original, ambitious objectives of the Euratom Treaty to be scaled back?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': "The complex and sensitive nature of the nuclear sector, which touched on Member States ' vital interests such as defence and national independence.",
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 6,
                          'text_span': 'owing to the complex and sensitive nature of the nuclear sector, which touched on the vital interests of the Member States (defence and national independence), those ambitions had to be scaled back'}],
        'difficulty': 'medium',
        'notes': 'Section 1.1.1, part b, on the Euratom Treaty. Classified as internal_market since it concerns a founding sectoral market policy rather than institutions.'
    },

    {
        'qa_id': 'internal_market_113',
        'question': 'What four common policies did the EEC Treaty of Rome originally provide for in the establishment of the European Economic Community?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'The elimination of customs duties between Member States, the establishment of an external Common Customs Tariff, common policies for agriculture and transport, and the creation of a European Social Fund (alongside the establishment of a European Investment Bank).',
        'gold_sources': [{'source': 'en-chapter-1.pdf',
                          'page': 5,
                          'text_span': "The elimination of customs duties between Member States; The establishment of an external Common Customs Tariff; The introduction of common policies for agriculture and transport"}],
        'difficulty': 'medium',
        'notes': 'Section 1.1.1, provisions of the EEC Treaty. Placed under internal_market as it defines the founding common-market provisions rather than an institutional matter.'
    },

    {
        'qa_id': 'economic_governance_103',
        'question': 'What is the primary objective of the European System of Central Banks (ESCB) under Article 127(1) TFEU?',
        'question_type': 'extractive',
        'topic_category': 'economic_governance',
        'gold_answer': 'To maintain price stability.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 287,
                          'text_span': 'The primary objective of the ESCB under Article 127(1) TFEU is to maintain price stability'}],
        'difficulty': 'easy',
        'notes': 'Section 2.6.3, Objectives.'
    },

    {
        'qa_id': 'economic_governance_104',
        'question': 'How does Article 130 TFEU protect the independence of the ECB?',
        'question_type': 'extractive',
        'topic_category': 'economic_governance',
        'gold_answer': 'It states that when exercising their powers and duties, neither the ECB, nor a national central bank, nor any member of their decision-making bodies shall seek or take instructions from Union institutions, Member State governments, or any other body.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 287,
                          'text_span': 'neither the ECB, nor a national central bank, nor any member of their decision-making bodies shall seek or take instructions from Union'}],
        'difficulty': 'medium',
        'notes': 'Section 2.6.3, Guiding principles, Independence.'
    },

    {
        'qa_id': 'economic_governance_105',
        'question': 'How often does the ECB publish a consolidated financial statement of the ESCB?',
        'question_type': 'extractive',
        'topic_category': 'economic_governance',
        'gold_answer': 'Each week.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 287,
                          'text_span': 'A consolidated financial statement of the ESCB is published each week'}],
        'difficulty': 'easy',
        'notes': 'Section 2.6.3, Guiding principles, Transparency and accountability.'
    },

    {
        'qa_id': 'economic_governance_106',
        'question': "Who holds the power to tax within the EU, and what is the EU 's role in tax policy?",
        'question_type': 'extractive',
        'topic_category': 'economic_governance',
        'gold_answer': 'The power to tax is in the hands of the Member States; the EU has only limited competences, with its tax policy geared towards the smooth running of the single market.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 313,
                          'text_span': 'The power to tax is in the hands of the Member States, with the EU having only limited competences'}],
        'difficulty': 'easy',
        'notes': 'Section 2.6.9, opening description.'
    },

    {
        'qa_id': 'economic_governance_107',
        'question': "How does the Council decide on tax measures under EU law, and what is Parliament 's role?",
        'question_type': 'extractive',
        'topic_category': 'economic_governance',
        'gold_answer': 'Tax measures must be adopted unanimously by the Member States in the Council; Parliament has the right to be consulted on tax matters, and for budgetary-related tax issues it is even co-legislator.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 313,
                          'text_span': 'Tax measures must be adopted unanimously by the Member States. The European Parliament has the right to be consulted on tax matters'}],
        'difficulty': 'medium',
        'notes': 'Section 2.6.9, opening description.'
    },

    {
        'qa_id': 'economic_governance_108',
        'question': 'Why was harmonisation of indirect taxation addressed before direct taxation in the EU?',
        'question_type': 'extractive',
        'topic_category': 'economic_governance',
        'gold_answer': 'Because EU tax policy is geared towards the smooth running of the single market, and indirect taxation has a more direct effect on that market than direct taxation.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 313,
                          'text_span': 'As the development of EU tax provisions is geared towards the smooth running of the single market, the harmonisation of indirect taxation was addressed at an earlier stage and in greater depth than that of direct taxation'}],
        'difficulty': 'medium',
        'notes': 'Section 2.6.9, direct/indirect taxation paragraph.'
    },

    {
        'qa_id': 'economic_governance_109',
        'question': 'What did the Commission propose regarding voting on tax matters, and what happened to that proposal?',
        'question_type': 'extractive',
        'topic_category': 'economic_governance',
        'gold_answer': 'The Commission proposed moving to qualified majority voting in certain tax areas, but the proposal was rejected by the Member States.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 313,
                          'text_span': 'the Commission submitted proposals for a move to qualified majority voting in certain tax areas. However, these were rejected by the Member States'}],
        'difficulty': 'medium',
        'notes': 'Section 2.6.9, tax provisions paragraph.'
    },

    {
        'qa_id': 'economic_governance_110',
        'question': "What is the relationship between the ECB 's independence and its accountability, and to which EU institution is it primarily accountable?",
        'question_type': 'synthesis',
        'topic_category': 'economic_governance',
        'gold_answer': "The ECB 's independence, guaranteed under Article 130 TFEU, is matched by accountability obligations: it must publish activity reports at least quarterly and a weekly consolidated financial statement, and under the TFEU it is primarily accountable to the European Parliament, though it also reports to the Council of the EU.",
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 287,
                          'text_span': 'Central bank independence is matched with accountability to the public and to its elected representatives'},
                          {'source': 'en-chapter-2.pdf',
                           'page': 287,
                           'text_span': 'the TFEU, the ECB is primarily accountable to'}],
        'difficulty': 'hard',
        'notes': 'Section 2.6.3, spans the page break between independence/transparency (p.287) and the accountability target named at the top of p.288.'
    },

    {
        'qa_id': 'sectoral_policy_103',
        'question': 'Where was the common fisheries policy (CFP) first formulated, and to which other policy was it originally linked?',
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'It was first formulated in the Treaty of Rome, and was initially linked to the common agricultural policy.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 90,
                          'text_span': 'A common fisheries policy (CFP) was first formulated in the Treaty of Rome. Initially linked to the common agricultural policy'}],
        'difficulty': 'easy',
        'notes': 'Section 3.3.1, opening description.'
    },

    {
        'qa_id': 'sectoral_policy_104',
        'question': 'What is the primary goal of the common fisheries policy, as revised in 2002?',
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'To ensure sustainable fisheries and guarantee incomes and stable jobs for fishers.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 90,
                          'text_span': 'The primary goal of the CFP, as revised in 2002, is to ensure sustainable fisheries and guarantee incomes and stable jobs for fishers'}],
        'difficulty': 'easy',
        'notes': 'Section 3.3.1, opening description.'
    },

    {
        'qa_id': 'sectoral_policy_105',
        'question': 'What change did the TFEU introduce regarding how legislation necessary for CFP objectives is adopted?',
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'Such legislation is now adopted under the ordinary legislative procedure (formerly codecision), making Parliament co-legislator, though it can only be adopted by the Council on the basis of a Commission proposal.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 90,
                          'text_span': 'legislation necessary for the pursuit of the objectives of the CFP is now adopted under the ordinary legislative procedure'}],
        'difficulty': 'medium',
        'notes': 'Section 3.3.1, Legal basis.'
    },

    {
        'qa_id': 'sectoral_policy_106',
        'question': 'When did the EU rail sector open up to competition, and how many legislative packages plus a recast were adopted in the following decade?',
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'The railway sector opened to competition in 2001; three packages and a recast were adopted over the following 10 years.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 164,
                          'text_span': 'Three packages and a recast were adopted in the space of 10 years following the opening-up of the railway sector to competition in 2001'}],
        'difficulty': 'medium',
        'notes': 'Section 3.4.5, opening description.'
    },

    {
        'qa_id': 'sectoral_policy_107',
        'question': "According to the Commission 's 2011 white paper on a Single European Transport Area, what is the target for medium-haul passenger transport by 2050?",
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'That the majority of medium-haul passenger transport should be carried out by rail by 2050.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 164,
                          'text_span': 'the goal of ensuring that the majority of medium-haul passenger transport is carried out by rail by 2050'}],
        'difficulty': 'medium',
        'notes': 'Section 3.4.5, Legal basis and objectives.'
    },

    {
        'qa_id': 'sectoral_policy_108',
        'question': "What two directives, adopted in 1996 and 2001, began the EU's process of ensuring interoperability between national rail networks?",
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'Directive 96/48/EC on the interoperability of the trans-European high-speed rail system, and Directive 2001/16/EC on the interoperability of the trans-European conventional rail system.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 164,
                          'text_span': 'Directive 96/48/EC of 23 July 1996 on the interoperability of the trans-European high-speed rail system and Directive 2001/16/EC of 19 March 2001 on the interoperability of the trans-European conventional rail system'}],
        'difficulty': 'hard',
        'notes': 'Section 3.4.5, Achievements, Interoperability. Two specific directive numbers -- good precision test for retrieval.'
    },

    {
        'qa_id': 'sectoral_policy_109',
        'question': 'What was the primary goal of the common fisheries policy before the 2002 reform added sustainability, compared to what the reform added?',
        'question_type': 'synthesis',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'The original CFP objectives were to preserve fish stocks, protect the marine environment, ensure the economic viability of EU fleets, and provide consumers with quality food. The 2002 reform added the sustainable use of living aquatic resources in an environmentally, economically and socially balanced way, based on sound scientific advice and the precautionary principle.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 90,
                          'text_span': 'The original objectives of the CFP were to preserve fish stocks, protect the marine environment, ensure the economic viability of EU fleets and provide consumers with quality food'},
                          {'source': 'en-chapter-3.pdf',
                           'page': 90,
                           'text_span': 'The 2002 reform added to these objectives the sustainable use of living aquatic resources'}],
        'difficulty': 'hard',
        'notes': 'Section 3.3.1, Objectives -- requires distinguishing original vs. 2002-added objectives, both stated on the same page.'
    },
    
    {
        'qa_id': 'sectoral_policy_110',
        'question': 'What did the Lisbon Treaty change about how international fisheries agreements are ratified?',
        'question_type': 'extractive',
        'topic_category': 'sectoral_policy',
        'gold_answer': 'It stipulated that international fisheries agreements are to be ratified by the Council after Parliament has given its consent.',
        'gold_sources': [{'source': 'en-chapter-3.pdf',
                          'page': 90,
                          'text_span': 'the Lisbon Treaty stipulates that they are to be ratified by the Council after Parliament has given its consent'}],
        'difficulty': 'medium',
        'notes': 'Section 3.3.1, Legal basis.'
    },

]
