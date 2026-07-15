QA_SET=[
    {
        'qa_id':'institution_101',
        'question':'What did the Treaty of Lisbon rename the Treaty establishing the European Community as?',
        'question_type':'extractive',
        'topic_catgeory':'insitutions',
        'gold_answer':'It was renamed the Treaty on the Functioning of the European Union (TFEU), and the term Community was replaced by Union throughout the text.',
        'gold_sources':[{'source':'en-chapter-1.pdf',
                        'page':21,
                        'text_span':'renamed the ‘Treaty on the Functioning of the European Union’ (TFEU) and the term ‘Community’ is replaced by ‘Union’ throughout the text'}],
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
        'question': 'Since which treaty has Parliament\'s assent been required for treaties admitting a new Member State?',
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
        'question': 'What are the EU\'s five main energy policy aims set out under the 2015 Energy Union strategy?',
        'question_type': 'extractive',
        'topic_category': 'internal_market',
        'gold_answer': 'Diversifying energy sources for security through EU solidarity; a fully integrated internal energy market; improving energy efficiency and cutting import dependence; decarbonising the economy in line with the Paris Agreement; and promoting research in low-carbon and clean energy technologies.',
        'gold_sources': [{'source': 'en-chapter-2.pdf',
                          'page': 203,
                          'text_span': 'five main aims of the EU’s energy policy'}],
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
        'notes': 'Deliberately mirrors the EPSO near-identical-fund-names distractor pattern (compare institutions_103\'s Council/European Council pair). Requires combining sections 3.1.3 and 3.1.4.'
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
                          'text_span': 'recognised codecision as the ‘ordinary legislative procedure’'}],
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
     }

]