(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/apps/web/app/abstraction-view.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AbstractionView",
    ()=>AbstractionView
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/evidence-views.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
const domains = [
    [
        "symptoms",
        "Symptoms and clinical course"
    ],
    [
        "function",
        "Functioning"
    ],
    [
        "treatment",
        "Treatment"
    ],
    [
        "measurement",
        "Measurements"
    ],
    [
        "plan",
        "Treatment plan"
    ],
    [
        "other",
        "Other findings"
    ]
];
function AbstractionView({ run, onSource }) {
    _s();
    const [tab, setTab] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("overview");
    const [reviewTarget, setReviewTarget] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "AbstractionView.useEffect": ()=>{
            if (tab !== "encounters" || !reviewTarget) return;
            const item = document.getElementById(`encounter-${encodeURIComponent(reviewTarget)}`);
            item?.setAttribute("open", "");
            item?.scrollIntoView({
                block: "center"
            });
        }
    }["AbstractionView.useEffect"], [
        tab,
        reviewTarget
    ]);
    const draft = run.result?.abstraction;
    if (!draft) return null;
    const citations = run.result?.citations ?? [];
    const calculations = run.result?.calculations;
    const concerns = draft.encounters.filter((event)=>event.disposition === "uncertain" || event.disposition === "included" && event.alternatives.length !== 1);
    const unusable = draft.coverage.filter((item)=>item.status === "unusable");
    const tabs = [
        [
            "overview",
            "Overview"
        ],
        [
            "encounters",
            `Encounters (${draft.encounters.length})`
        ],
        [
            "evidence",
            "Sources & structured data"
        ]
    ];
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "abstraction-tabs",
                role: "tablist",
                "aria-label": "Abstraction views",
                children: tabs.map(([id, label])=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        role: "tab",
                        id: `abstraction-tab-${id}`,
                        "aria-selected": tab === id,
                        "aria-controls": `abstraction-panel-${id}`,
                        onClick: ()=>setTab(id),
                        children: label
                    }, id, false, {
                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                        lineNumber: 58,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                lineNumber: 52,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                role: "tabpanel",
                id: `abstraction-panel-${tab}`,
                "aria-labelledby": `abstraction-tab-${tab}`,
                children: [
                    tab === "overview" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "abstraction-overview-stats",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                children: [
                                                    draft.coverage.length - unusable.length,
                                                    "/",
                                                    draft.coverage.length
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 79,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                children: "sources represented"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 83,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 78,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                children: draft.encounters.length
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 86,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                children: "documented encounters"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 87,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 85,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                children: concerns.length + unusable.length
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 90,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                children: "unresolved event / source issues"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 91,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 89,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 77,
                                columnNumber: 13
                            }, this),
                            (concerns.length > 0 || unusable.length > 0) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                                className: "abstraction-review",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                        children: "Needs review"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 96,
                                        columnNumber: 17
                                    }, this),
                                    concerns.map((event)=>{
                                        const contribution = calculations?.contributions.find((row)=>row.encounter_id === event.encounter_id);
                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "review-item",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                            children: [
                                                                event.date,
                                                                " · ",
                                                                event.modality
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 104,
                                                            columnNumber: 25
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            children: event.disposition === "uncertain" ? "Attendance or eligibility is unresolved." : event.alternatives.length > 1 ? `Competing source accounts: ${contribution && contribution.seconds.length > 1 ? (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["minutes"])(contribution.seconds) : "different accounts of patient contact"}.` : "Patient-contact duration is unknown."
                                                        }, void 0, false, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 107,
                                                            columnNumber: 25
                                                        }, this)
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                    lineNumber: 103,
                                                    columnNumber: 23
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                    className: "secondary",
                                                    onClick: ()=>{
                                                        setReviewTarget(event.encounter_id);
                                                        setTab("encounters");
                                                    },
                                                    children: "Inspect accounts →"
                                                }, void 0, false, {
                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                    lineNumber: 115,
                                                    columnNumber: 23
                                                }, this)
                                            ]
                                        }, event.encounter_id, true, {
                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                            lineNumber: 102,
                                            columnNumber: 21
                                        }, this);
                                    }),
                                    unusable.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            children: [
                                                "Source gap: ",
                                                item.note
                                            ]
                                        }, item.revision_id, true, {
                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                            lineNumber: 128,
                                            columnNumber: 19
                                        }, this))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 95,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                className: "clinical-section-title",
                                children: "Clinical overview"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 132,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "muted-text",
                                children: "Extracted findings grouped by clinical topic. Expand a topic or source to inspect the supporting record."
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 133,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "clinical-topics",
                                children: domains.map(([category, label])=>{
                                    const findings = draft.findings.filter((claim)=>claim.category === category);
                                    if (!findings.length) return null;
                                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                        className: "clinical-topic",
                                        open: category === "symptoms" || category === "function",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                children: [
                                                    label,
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        className: "count",
                                                        children: findings.length
                                                    }, void 0, false, {
                                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                        lineNumber: 151,
                                                        columnNumber: 23
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 149,
                                                columnNumber: 21
                                            }, this),
                                            findings.map((claim, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            children: claim.text
                                                        }, void 0, false, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 155,
                                                            columnNumber: 25
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                                            className: "finding-sources",
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                                    children: "Supporting sources"
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                                    lineNumber: 157,
                                                                    columnNumber: 27
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                                    ids: claim.citations,
                                                                    citations: citations,
                                                                    onSource: onSource
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                                    lineNumber: 158,
                                                                    columnNumber: 27
                                                                }, this)
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 156,
                                                            columnNumber: 25
                                                        }, this)
                                                    ]
                                                }, index, true, {
                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                    lineNumber: 154,
                                                    columnNumber: 23
                                                }, this))
                                        ]
                                    }, category, true, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 144,
                                        columnNumber: 19
                                    }, this);
                                })
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 137,
                                columnNumber: 13
                            }, this),
                            draft.limitations.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                className: "coverage-details",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                        children: [
                                            "Additional uncertainty and limitations (",
                                            draft.limitations.length,
                                            ")"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 172,
                                        columnNumber: 17
                                    }, this),
                                    draft.limitations.map((limitation, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            children: limitation
                                        }, index, false, {
                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                            lineNumber: 177,
                                            columnNumber: 19
                                        }, this))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 171,
                                columnNumber: 15
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                        lineNumber: 76,
                        columnNumber: 11
                    }, this),
                    tab === "encounters" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                className: "clinical-section-title",
                                children: "Encounter ledger"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 185,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "muted-text",
                                children: "One row per encounter. Included and excluded contacts stay visible; expand a row for time intervals and competing source accounts."
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 186,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "encounter-list",
                                children: [
                                    ...draft.encounters
                                ].sort((a, b)=>a.date.localeCompare(b.date) || a.encounter_id.localeCompare(b.encounter_id)).map((event)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                        className: "encounter",
                                        id: `encounter-${encodeURIComponent(event.encounter_id)}`,
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                                children: event.date
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                                lineNumber: 206,
                                                                columnNumber: 25
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                                                children: [
                                                                    event.encounter_id,
                                                                    " · ",
                                                                    event.modality
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                                lineNumber: 207,
                                                                columnNumber: 25
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                        lineNumber: 205,
                                                        columnNumber: 23
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        className: `disposition ${event.disposition}`,
                                                        children: event.disposition
                                                    }, void 0, false, {
                                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                        lineNumber: 211,
                                                        columnNumber: 23
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                        children: event.disposition === "excluded" ? "—" : (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["minutes"])(run.result?.calculations?.contributions.find((row)=>row.encounter_id === event.encounter_id)?.seconds ?? [])
                                                    }, void 0, false, {
                                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                        lineNumber: 214,
                                                        columnNumber: 23
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 204,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                children: event.explanation
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 225,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                ids: event.citations,
                                                citations: citations,
                                                onSource: onSource
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 226,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h4", {
                                                children: "Source accounts"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 231,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Findings"], {
                                                claims: event.source_accounts,
                                                citations: citations,
                                                onSource: onSource
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                lineNumber: 232,
                                                columnNumber: 21
                                            }, this),
                                            event.alternatives.map((account, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                    className: "duration-account",
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                            children: event.alternatives.length > 1 ? `Alternative ${index + 1}` : "Time basis"
                                                        }, void 0, false, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 239,
                                                            columnNumber: 25
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            children: account.basis
                                                        }, void 0, false, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 244,
                                                            columnNumber: 25
                                                        }, this),
                                                        account.stated_minutes !== null ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            children: [
                                                                "Explicit patient contact: ",
                                                                account.stated_minutes,
                                                                " ",
                                                                "min"
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 246,
                                                            columnNumber: 27
                                                        }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                    children: [
                                                                        "Contact:",
                                                                        " ",
                                                                        account.contact.map((v)=>`${v.start}–${v.end}`).join(", ")
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                                    lineNumber: 252,
                                                                    columnNumber: 29
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                    children: [
                                                                        "Patient present:",
                                                                        " ",
                                                                        account.patient_presence.map((v)=>`${v.start}–${v.end}`).join(", ")
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                                    lineNumber: 258,
                                                                    columnNumber: 29
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                    children: [
                                                                        "Breaks:",
                                                                        " ",
                                                                        account.breaks.map((v)=>`${v.start}–${v.end}`).join(", ") || "None documented"
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                                    lineNumber: 264,
                                                                    columnNumber: 29
                                                                }, this)
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 251,
                                                            columnNumber: 27
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                            ids: account.citations,
                                                            citations: citations,
                                                            onSource: onSource
                                                        }, void 0, false, {
                                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                            lineNumber: 272,
                                                            columnNumber: 25
                                                        }, this)
                                                    ]
                                                }, index, true, {
                                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                                    lineNumber: 238,
                                                    columnNumber: 23
                                                }, this))
                                        ]
                                    }, event.encounter_id, true, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 199,
                                        columnNumber: 19
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 191,
                                columnNumber: 13
                            }, this),
                            calculations && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                className: "coverage-details",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                        children: "Treatment totals, weekly goals, and calculation details"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 285,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Calculated"], {
                                        value: calculations,
                                        citations: citations,
                                        onSource: onSource
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 288,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 284,
                                columnNumber: 15
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                        lineNumber: 184,
                        columnNumber: 11
                    }, this),
                    tab === "evidence" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                className: "clinical-section-title",
                                children: "Source coverage"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 299,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "muted-text",
                                children: "Coverage refers to this source snapshot. It does not establish that the full clinical record is complete."
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 300,
                                columnNumber: 13
                            }, this),
                            draft.coverage.map((item, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                    className: "coverage-record",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>onSource(item.revision_id, ""),
                                            children: [
                                                citations.find((citation)=>citation.revision_id === item.revision_id)?.filename ?? `Source ${index + 1}`,
                                                " ",
                                                "↗"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                            lineNumber: 306,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            children: item.status === "reviewed" ? "Represented in draft" : "Needs review"
                                        }, void 0, false, {
                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                            lineNumber: 312,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            children: item.note
                                        }, void 0, false, {
                                            fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                            lineNumber: 317,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, item.revision_id, true, {
                                    fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                    lineNumber: 305,
                                    columnNumber: 15
                                }, this)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                className: "coverage-details",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                        children: "Inspect structured abstraction JSON"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 321,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        children: "Machine-readable draft: encounters, duration alternatives, findings, plan rules, and source references. Clinical findings are currently text claims, not a fully normalized clinical record."
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 322,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                                        className: "abstraction-json",
                                        children: JSON.stringify(draft, null, 2)
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                        lineNumber: 328,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                                lineNumber: 320,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/abstraction-view.tsx",
                        lineNumber: 298,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/abstraction-view.tsx",
                lineNumber: 70,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/abstraction-view.tsx",
        lineNumber: 51,
        columnNumber: 5
    }, this);
}
_s(AbstractionView, "4DqBBePZGehkNLateGJNyHFQmNk=");
_c = AbstractionView;
var _c;
__turbopack_context__.k.register(_c, "AbstractionView");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/app/answer-view.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AnswerBody",
    ()=>AnswerBody
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/evidence-views.tsx [app-client] (ecmascript)");
"use client";
;
;
const shortDate = (value)=>new Intl.DateTimeFormat("en-US", {
        month: "short",
        day: "numeric",
        timeZone: "UTC"
    }).format(new Date(`${value}T12:00:00Z`));
function AnswerBody({ result, onSource }) {
    const answer = result.answer;
    if (!answer) return null;
    const value = result.calculations;
    const unresolved = value?.contributions.filter((row)=>row.disposition !== "excluded" && (row.disposition === "uncertain" || row.seconds.length !== 1)) ?? [];
    const sharedGoal = value?.weeks[0];
    const sameGoal = sharedGoal && value?.weeks.every((week)=>week.minimum_days === sharedGoal.minimum_days && week.minimum_minutes === sharedGoal.minimum_minutes);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "answer-summary",
                children: value ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "answer-lead",
                            children: value.total.sessions !== null && value.total.days !== null ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: [
                                            value.total.sessions,
                                            " ",
                                            value.total.sessions === 1 ? "session" : "sessions"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/answer-view.tsx",
                                        lineNumber: 44,
                                        columnNumber: 19
                                    }, this),
                                    " ",
                                    "across",
                                    " ",
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: [
                                            value.total.days,
                                            " treatment",
                                            " ",
                                            value.total.days === 1 ? "day" : "days"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/answer-view.tsx",
                                        lineNumber: 49,
                                        columnNumber: 19
                                    }, this),
                                    ",",
                                    " ",
                                    value.total.complete ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                        children: [
                                            "totaling ",
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["minutes"])(value.total.seconds)
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/answer-view.tsx",
                                                lineNumber: 56,
                                                columnNumber: 32
                                            }, this),
                                            "."
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/answer-view.tsx",
                                        lineNumber: 55,
                                        columnNumber: 21
                                    }, this) : "with treatment time still undetermined."
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/answer-view.tsx",
                                lineNumber: 43,
                                columnNumber: 17
                            }, this) : "A complete total cannot be determined from the available evidence."
                        }, void 0, false, {
                            fileName: "[project]/apps/web/app/answer-view.tsx",
                            lineNumber: 41,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "answer-scope",
                            children: [
                                value.total.start,
                                " – ",
                                value.total.end
                            ]
                        }, void 0, true, {
                            fileName: "[project]/apps/web/app/answer-view.tsx",
                            lineNumber: 66,
                            columnNumber: 13
                        }, this),
                        value.weeks.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    className: "answer-goal",
                                    children: sameGoal ? `Weekly goal: at least ${sharedGoal.minimum_days} days and ${sharedGoal.minimum_minutes} minutes.` : "Weekly treatment goals:"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/answer-view.tsx",
                                    lineNumber: 71,
                                    columnNumber: 17
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                                    className: "answer-weeks",
                                    children: value.weeks.map((week, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: [
                                                        shortDate(week.start),
                                                        " – ",
                                                        shortDate(week.end),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                                            children: [
                                                                week.days ?? "Unknown",
                                                                " days ·",
                                                                " ",
                                                                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["minutes"])(week.seconds),
                                                                !sameGoal && ` · Goal: ${week.minimum_days} days and ${week.minimum_minutes} min`
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/apps/web/app/answer-view.tsx",
                                                            lineNumber: 81,
                                                            columnNumber: 25
                                                        }, this)
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/apps/web/app/answer-view.tsx",
                                                    lineNumber: 79,
                                                    columnNumber: 23
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                    className: `disposition ${week.goal_status}`,
                                                    children: week.goal_status === "met" ? "Met" : week.goal_status === "not_met" ? "Not met" : "Cannot determine"
                                                }, void 0, false, {
                                                    fileName: "[project]/apps/web/app/answer-view.tsx",
                                                    lineNumber: 88,
                                                    columnNumber: 23
                                                }, this)
                                            ]
                                        }, index, true, {
                                            fileName: "[project]/apps/web/app/answer-view.tsx",
                                            lineNumber: 78,
                                            columnNumber: 21
                                        }, this))
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/answer-view.tsx",
                                    lineNumber: 76,
                                    columnNumber: 17
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/apps/web/app/answer-view.tsx",
                            lineNumber: 70,
                            columnNumber: 15
                        }, this),
                        unresolved.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "answer-uncertainty",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                    children: "Why the uncertainty?"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/answer-view.tsx",
                                    lineNumber: 102,
                                    columnNumber: 17
                                }, this),
                                unresolved.map((row)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        children: [
                                            shortDate(row.date),
                                            ":",
                                            " ",
                                            row.seconds.length > 1 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                                children: [
                                                    "conflicting accounts document",
                                                    " ",
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                        children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["minutes"])(row.seconds)
                                                    }, void 0, false, {
                                                        fileName: "[project]/apps/web/app/answer-view.tsx",
                                                        lineNumber: 109,
                                                        columnNumber: 25
                                                    }, this),
                                                    " for the same encounter."
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/answer-view.tsx",
                                                lineNumber: 107,
                                                columnNumber: 23
                                            }, this) : row.disposition === "uncertain" ? "attendance or eligibility is uncertain." : "patient-contact duration is unknown."
                                        ]
                                    }, row.encounter_id, true, {
                                        fileName: "[project]/apps/web/app/answer-view.tsx",
                                        lineNumber: 104,
                                        columnNumber: 19
                                    }, this))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/apps/web/app/answer-view.tsx",
                            lineNumber: 101,
                            columnNumber: 15
                        }, this),
                        !value.total.complete && unresolved.length === 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "answer-uncertainty",
                            children: "Source coverage is incomplete. Review the evidence before using these totals."
                        }, void 0, false, {
                            fileName: "[project]/apps/web/app/answer-view.tsx",
                            lineNumber: 122,
                            columnNumber: 15
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/apps/web/app/answer-view.tsx",
                    lineNumber: 40,
                    columnNumber: 11
                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                    children: [
                        answer.statements.slice(0, 3).map((claim, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "answer-narrative",
                                children: claim.text
                            }, index, false, {
                                fileName: "[project]/apps/web/app/answer-view.tsx",
                                lineNumber: 131,
                                columnNumber: 15
                            }, this)),
                        answer.limitations.slice(0, 2).map((limitation, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "answer-uncertainty",
                                children: limitation
                            }, index, false, {
                                fileName: "[project]/apps/web/app/answer-view.tsx",
                                lineNumber: 136,
                                columnNumber: 15
                            }, this)),
                        !answer.statements.length && !answer.limitations.length && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            children: "The available records do not support an answer to this question."
                        }, void 0, false, {
                            fileName: "[project]/apps/web/app/answer-view.tsx",
                            lineNumber: 141,
                            columnNumber: 15
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/apps/web/app/answer-view.tsx",
                    lineNumber: 129,
                    columnNumber: 11
                }, this)
            }, void 0, false, {
                fileName: "[project]/apps/web/app/answer-view.tsx",
                lineNumber: 38,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                className: "answer-evidence",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                        children: "View explanation, sources, and calculation details"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/answer-view.tsx",
                        lineNumber: 149,
                        columnNumber: 9
                    }, this),
                    answer.statements.map((claim, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "finding",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    children: claim.text
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/answer-view.tsx",
                                    lineNumber: 152,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                    ids: claim.citations,
                                    citations: result.citations,
                                    onSource: onSource
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/answer-view.tsx",
                                    lineNumber: 153,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, index, true, {
                            fileName: "[project]/apps/web/app/answer-view.tsx",
                            lineNumber: 151,
                            columnNumber: 11
                        }, this)),
                    value && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Calculated"], {
                        value: value,
                        citations: result.citations,
                        onSource: onSource
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/answer-view.tsx",
                        lineNumber: 161,
                        columnNumber: 11
                    }, this),
                    answer.limitations.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "answer-qualifications",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h4", {
                                children: "Limitations"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/answer-view.tsx",
                                lineNumber: 169,
                                columnNumber: 13
                            }, this),
                            answer.limitations.map((limitation, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    children: limitation
                                }, index, false, {
                                    fileName: "[project]/apps/web/app/answer-view.tsx",
                                    lineNumber: 171,
                                    columnNumber: 15
                                }, this))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/answer-view.tsx",
                        lineNumber: 168,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/answer-view.tsx",
                lineNumber: 148,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/answer-view.tsx",
        lineNumber: 37,
        columnNumber: 5
    }, this);
}
_c = AnswerBody;
var _c;
__turbopack_context__.k.register(_c, "AnswerBody");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/app/clinical-panel.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ClinicalPanel",
    ()=>ClinicalPanel
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/lib/api.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/evidence-views.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$answer$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/answer-view.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$abstraction$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/abstraction-view.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$document$2d$timeline$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/document-timeline.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$readable$2d$abstraction$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/readable-abstraction-view.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$course$2d$of$2d$care$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/course-of-care-view.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
;
;
;
;
;
function ClinicalPanel({ patientId, csrf, snapshot, snapshots, onSnapshot, view, onSource }) {
    _s();
    const [runs, setRuns] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [model, setModel] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [selected, setSelected] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [question, setQuestion] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [error, setError] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [sending, setSending] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [loading, setLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(true);
    const retry = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    const loadedVersion = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])("");
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ClinicalPanel.useEffect": ()=>{
            let disposed = false;
            let timer;
            loadedVersion.current = "";
            const poll = {
                "ClinicalPanel.useEffect.poll": async ()=>{
                    try {
                        // Poll a small change marker; download full results only when something changed.
                        const { version } = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])(`/patients/${patientId}/analyses/version`);
                        if (version !== loadedVersion.current) {
                            const [values, status] = await Promise.all([
                                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["allPages"])(`/patients/${patientId}/analyses`),
                                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])("/model-status")
                            ]);
                            if (!disposed) {
                                loadedVersion.current = version;
                                setRuns(values.sort({
                                    "ClinicalPanel.useEffect.poll": (a, b)=>b.created_at.localeCompare(a.created_at)
                                }["ClinicalPanel.useEffect.poll"]));
                                setModel(status);
                            }
                        }
                        if (!disposed) setLoading(false);
                    } catch (e) {
                        if (!disposed) {
                            setError(e instanceof Error ? e.message : "Unable to load analysis");
                            setLoading(false);
                        }
                    }
                    if (!disposed) timer = setTimeout(poll, 2500);
                }
            }["ClinicalPanel.useEffect.poll"];
            void poll();
            return ({
                "ClinicalPanel.useEffect": ()=>{
                    disposed = true;
                    clearTimeout(timer);
                }
            })["ClinicalPanel.useEffect"];
        }
    }["ClinicalPanel.useEffect"], [
        patientId
    ]);
    const matching = runs.filter((run)=>run.snapshot_id === snapshot?.id);
    const documentRuns = matching.filter((run)=>!!run.result?.document_catalog && run.status === "succeeded");
    const documentRun = documentRuns.find((run)=>run.id === selected) ?? documentRuns[0];
    const displayedRuns = view === "documents" ? documentRuns : matching.filter((run)=>run.kind === "abstraction" && run.status === "succeeded");
    const abstractions = matching.filter((run)=>run.kind === "abstraction" && run.status === "succeeded");
    const abstraction = abstractions.find((run)=>run.id === selected) ?? abstractions[0];
    const draft = abstraction?.result?.abstraction;
    const readable = abstraction?.result?.readable_abstraction;
    const checkedSources = new Set(readable?.reviews?.filter((review)=>review.status === "checked").map((review)=>review.target_ref));
    const canAsk = readable?.documents.some((document)=>checkedSources.has(document.profile.revision_id)) ?? false;
    const active = runs.find((run)=>[
            "queued",
            "running"
        ].includes(run.status));
    const answers = matching.filter((run)=>run.kind === "answer" && run.abstraction_id === abstraction?.id);
    async function submit(kind) {
        if (!snapshot || kind === "answer" && (!question.trim() || !abstraction)) return;
        setSending(true);
        setError("");
        const payload = {
            snapshot_id: snapshot.id,
            ...kind === "documents" ? {
                document_catalog: true
            } : {},
            ...kind === "answer" ? {
                abstraction_id: abstraction.id,
                question: question.trim()
            } : {}
        };
        const signature = JSON.stringify(payload);
        if (retry.current?.signature !== signature) retry.current = {
            signature,
            key: crypto.randomUUID()
        };
        try {
            const run = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])(`/patients/${patientId}/analyses`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-Token": csrf,
                    "Idempotency-Key": retry.current.key
                },
                body: signature
            });
            setRuns((current)=>[
                    run,
                    ...current.filter((value)=>value.id !== run.id)
                ]);
            retry.current = null;
            if (kind === "answer") setQuestion("");
            else setSelected("");
        } catch (e) {
            setError(e instanceof Error ? e.message : "Unable to start analysis");
        } finally{
            setSending(false);
        }
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        className: "panel clinical-panel",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "clinical-heading",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "eyebrow",
                                children: "CLAUDE · SOURCE-LINKED DRAFT"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 160,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                children: view === "documents" ? "Document timeline" : view === "abstraction" ? "Clinical abstraction" : "Ask the record"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 161,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                children: view === "documents" ? "Inspect what each record is, who contributed or signed it, and its history." : view === "abstraction" ? "Inspect encounters, conflicting accounts, and the clinical course." : "Ask a question about this patient's selected source snapshot."
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 168,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 159,
                        columnNumber: 9
                    }, this),
                    view !== "abstraction" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        className: "snapshot-picker",
                        children: [
                            "Source snapshot",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                "aria-label": "Analysis source snapshot",
                                value: snapshot?.id ?? "",
                                onChange: (event)=>{
                                    onSnapshot(event.target.value);
                                    setSelected("");
                                },
                                children: snapshots.map((value)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: value.id,
                                        children: [
                                            "v",
                                            value.sequence,
                                            " · ",
                                            value.manifest.length,
                                            " sources"
                                        ]
                                    }, value.id, true, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 188,
                                        columnNumber: 17
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 179,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 177,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 158,
                columnNumber: 7
            }, this),
            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "alert error",
                role: "alert",
                children: error
            }, void 0, false, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 197,
                columnNumber: 9
            }, this),
            view !== "abstraction" && snapshot && snapshot.id !== snapshots[0]?.id && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "alert warning",
                children: "Historical snapshot. Newer imports are not included."
            }, void 0, false, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 204,
                columnNumber: 11
            }, this),
            model && !model.configured && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "alert warning",
                children: "Claude is not configured. Add EHR_ANTHROPIC_API_KEY to the server’s .env file and restart the services."
            }, void 0, false, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 209,
                columnNumber: 9
            }, this),
            view !== "ask" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "analysis-actions",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: model?.model ?? "Checking Claude configuration…"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 216,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: "primary",
                        disabled: loading || !model?.configured || !snapshot || !!active || sending,
                        onClick: ()=>void submit(view === "documents" ? "documents" : "abstraction"),
                        children: sending ? "Starting…" : view === "documents" ? documentRun ? "Refresh document timeline" : "Generate document timeline" : draft ? "Run new abstraction" : "Generate abstraction"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 217,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 215,
                columnNumber: 9
            }, this),
            active && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "alert",
                role: "status",
                children: [
                    active.kind === "documents" ? "Extracting document metadata with Claude" : active.kind === "abstraction" ? "Extracting, checking and reconciling sources with Claude" : "Preparing a cited answer",
                    " ",
                    "· ",
                    active.status,
                    ". You can leave this page and return later.",
                    active.progress && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        children: [
                            active.progress.validated_documents,
                            " of",
                            " ",
                            active.progress.total_documents,
                            " documents processed",
                            active.progress.failed_documents > 0 && ` · ${active.progress.failed_documents} need attention`,
                            active.progress.validated_documents + active.progress.failed_documents === active.progress.total_documents && active.kind === "abstraction" && " · Preparing reconciliation proposals"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 247,
                        columnNumber: 13
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 239,
                columnNumber: 9
            }, this),
            matching.filter((run)=>run.kind === (view === "documents" ? "documents" : "abstraction")).slice(0, 1).filter((run)=>run.status === "failed").map((run)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "alert warning",
                    children: [
                        view === "documents" ? "Document metadata" : "Abstraction",
                        " failed:",
                        " ",
                        (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(run.error_code ?? "processing failed"),
                        ". Correct the issue, then start a new run."
                    ]
                }, run.id, true, {
                    fileName: "[project]/apps/web/app/clinical-panel.tsx",
                    lineNumber: 269,
                    columnNumber: 11
                }, this)),
            displayedRuns.length > 1 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: "run-picker",
                children: [
                    view === "documents" ? "Document metadata version" : "Abstraction version",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                        "aria-label": view === "documents" ? "Document metadata version" : "Abstraction version",
                        value: (view === "documents" ? documentRun : abstraction)?.id ?? "",
                        onChange: (event)=>setSelected(event.target.value),
                        children: displayedRuns.map((run)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                value: run.id,
                                children: new Date(run.created_at).toLocaleString()
                            }, run.id, false, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 290,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 280,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 276,
                columnNumber: 9
            }, this),
            view === "documents" ? documentRun ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$document$2d$timeline$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["DocumentTimeline"], {
                        run: documentRun,
                        patientId: patientId,
                        onSource: onSource
                    }, documentRun.id, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 300,
                        columnNumber: 13
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "analysis-provenance",
                        children: [
                            documentRun.model,
                            " · ",
                            documentRun.prompt_version,
                            " ·",
                            " ",
                            new Date(documentRun.created_at).toLocaleString()
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 306,
                        columnNumber: 13
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 299,
                columnNumber: 11
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "empty",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                        children: loading ? "Loading document history…" : "Document metadata has not been extracted"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 313,
                        columnNumber: 13
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        children: "Generate the timeline from this snapshot. This sends the selected fictional records to Anthropic and preserves your existing clinical abstraction."
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 318,
                        columnNumber: 13
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 312,
                columnNumber: 11
            }, this) : !draft ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "empty",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                        children: loading ? "Loading analysis…" : "Sources are ready for abstraction"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 327,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        children: "Generate an abstraction to review the evidence and ask questions. This sends the selected fictional records to Anthropic."
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 332,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 326,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "draft-notice",
                        children: [
                            "Unreviewed AI draft ·",
                            " ",
                            draft.coverage.filter((item)=>item.status === "reviewed").length,
                            "/",
                            snapshot?.manifest.length,
                            " sources represented · Source links are verified; clinical interpretations still need review."
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 339,
                        columnNumber: 11
                    }, this),
                    !abstraction.result?.readable_abstraction && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "alert warning",
                        children: "This is an older abstraction format. Run a new abstraction to use the readable view and updated querying."
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 346,
                        columnNumber: 13
                    }, this),
                    view === "abstraction" ? abstraction.result?.readable_abstraction ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$course$2d$of$2d$care$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["CourseOfCareView"], {
                                patientId: patientId,
                                runId: abstraction.id,
                                onSource: onSource
                            }, `${abstraction.id}-course`, false, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 354,
                                columnNumber: 17
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                className: "encounter-ledger",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                        children: "Per-document abstractions"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 361,
                                        columnNumber: 19
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$readable$2d$abstraction$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ReadableAbstractionView"], {
                                        run: abstraction,
                                        onSource: onSource
                                    }, abstraction.id, false, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 362,
                                        columnNumber: 19
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 360,
                                columnNumber: 17
                            }, this),
                            draft.encounters.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                className: "encounter-ledger",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                        children: [
                                            "Encounter ledger and calculated totals (",
                                            draft.encounters.length,
                                            " encounters)"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 370,
                                        columnNumber: 21
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$abstraction$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AbstractionView"], {
                                        run: abstraction,
                                        onSource: onSource
                                    }, `${abstraction.id}-ledger`, false, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 374,
                                        columnNumber: 21
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 369,
                                columnNumber: 19
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 353,
                        columnNumber: 15
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$abstraction$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AbstractionView"], {
                        run: abstraction,
                        onSource: onSource
                    }, abstraction.id, false, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 383,
                        columnNumber: 15
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                                className: "question-form",
                                onSubmit: (event)=>{
                                    event.preventDefault();
                                    void submit("answer");
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                        htmlFor: "clinical-question",
                                        children: "Your question"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 398,
                                        columnNumber: 17
                                    }, this),
                                    !canAsk && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "muted-text",
                                        children: "Source checks are still needed before querying. Re-run the abstraction to retry flagged sources."
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 400,
                                        columnNumber: 19
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
                                        id: "clinical-question",
                                        rows: 3,
                                        maxLength: 2000,
                                        placeholder: "What changed over the review period? Which treatment time is uncertain?",
                                        value: question,
                                        onChange: (event)=>setQuestion(event.target.value)
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 405,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "question-examples",
                                        children: [
                                            "How many sessions, days, and minutes of care are documented?",
                                            "Were the documented weekly treatment goals met?",
                                            "Summarize changes in symptoms and functioning."
                                        ].map((value)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                type: "button",
                                                onClick: ()=>setQuestion(value),
                                                children: value
                                            }, value, false, {
                                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                                lineNumber: 419,
                                                columnNumber: 21
                                            }, this))
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 413,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "primary",
                                        disabled: !question.trim() || !canAsk || !!active || sending || !model?.configured,
                                        children: "Ask"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 428,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 391,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "answer-history",
                                children: answers.map((run)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                        className: "answer-card",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                className: "eyebrow",
                                                children: [
                                                    new Date(run.created_at).toLocaleString(),
                                                    " ·",
                                                    " ",
                                                    run.result?.answer?.status ?? run.status
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                                lineNumber: 444,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                                children: run.question
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                                lineNumber: 448,
                                                columnNumber: 21
                                            }, this),
                                            run.error_code && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "alert warning",
                                                children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(run.error_code)
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                                lineNumber: 450,
                                                columnNumber: 23
                                            }, this),
                                            run.result?.answer && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$answer$2d$view$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AnswerBody"], {
                                                result: run.result,
                                                onSource: onSource
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                                lineNumber: 453,
                                                columnNumber: 23
                                            }, this),
                                            [
                                                "queued",
                                                "running"
                                            ].includes(run.status) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                role: "status",
                                                children: "Preparing answer…"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                                lineNumber: 456,
                                                columnNumber: 23
                                            }, this)
                                        ]
                                    }, run.id, true, {
                                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                        lineNumber: 443,
                                        columnNumber: 19
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                                lineNumber: 441,
                                columnNumber: 15
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 390,
                        columnNumber: 13
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "analysis-provenance",
                        children: [
                            abstraction.model,
                            " · ",
                            abstraction.prompt_version,
                            " ·",
                            " ",
                            new Date(abstraction.created_at).toLocaleString(),
                            " ·",
                            " ",
                            abstraction.usage?.input_tokens.toLocaleString(),
                            " input /",
                            " ",
                            abstraction.usage?.output_tokens.toLocaleString(),
                            " output tokens"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/clinical-panel.tsx",
                        lineNumber: 463,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/clinical-panel.tsx",
                lineNumber: 338,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/clinical-panel.tsx",
        lineNumber: 157,
        columnNumber: 5
    }, this);
}
_s(ClinicalPanel, "eowARomk38R+dnxh4L2LdTt8EPc=");
_c = ClinicalPanel;
var _c;
__turbopack_context__.k.register(_c, "ClinicalPanel");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/app/course-of-care-view.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "CourseOfCareView",
    ()=>CourseOfCareView
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/lib/api.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/evidence-views.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
const STATUS_LABEL = {
    documented: "Documented",
    established: "Established",
    corroborated: "Corroborated",
    conflicting: "Conflicting",
    superseded: "Superseded",
    uncertain: "Uncertain",
    not_documented: "Not documented",
    inferred: "Inferred"
};
const OPEN = new Set([
    "conflicting",
    "uncertain",
    "not_documented",
    "inferred"
]);
const GROUPS = {
    All: ()=>true,
    Encounters: (a)=>a.subject_type === "encounter",
    Assessments: (a)=>a.subject_type === "assessment",
    Goals: (a)=>a.subject_type === "goal",
    Findings: (a)=>a.kind === "finding",
    Medication: (a)=>a.value?.type === "medication",
    "Patient-reported": (a)=>a.value?.reporter === "patient",
    Collateral: (a)=>a.value?.reporter === "collateral"
};
function Badge({ status }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
        className: `status-badge ${status}`,
        children: STATUS_LABEL[status] ?? status
    }, void 0, false, {
        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
        lineNumber: 40,
        columnNumber: 5
    }, this);
}
_c = Badge;
function Row({ assertion, record, onSource }) {
    const names = new Map(record.documents.map((d)=>[
            d.revision_id,
            d.filename
        ]));
    const rule = assertion.resolution?.rule;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
        className: `assertion ${assertion.status}`,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "assertion-head",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Badge, {
                        status: assertion.status
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 62,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "assertion-kind",
                        children: assertion.kind.replaceAll("_", " ")
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 63,
                        columnNumber: 9
                    }, this),
                    assertion.subject !== "patient" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "assertion-subject",
                        children: assertion.subject
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 67,
                        columnNumber: 11
                    }, this),
                    typeof assertion.value?.type === "string" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "assertion-kind",
                        children: String(assertion.value.type).replaceAll("_", " ")
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 70,
                        columnNumber: 11
                    }, this),
                    typeof assertion.value?.reporter === "string" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "assertion-kind",
                        children: [
                            "reported by ",
                            String(assertion.value.reporter)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 75,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 61,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                children: assertion.text
            }, void 0, false, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 80,
                columnNumber: 7
            }, this),
            assertion.resolution && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "assertion-rule",
                title: record.rules[rule ?? ""] ?? "",
                children: [
                    "Resolution: ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                        children: rule?.replaceAll("_", " ")
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 83,
                        columnNumber: 23
                    }, this),
                    " —",
                    " ",
                    assertion.resolution.reason
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 82,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "evidence-links",
                children: assertion.evidence.map((e)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: e.stance === "contradicts" ? "contradicts" : "",
                        title: e.stance,
                        onClick: ()=>onSource(e.revision_id, e.span_id),
                        children: [
                            e.stance === "contradicts" ? "✕ " : "",
                            (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["sourceLabel"])(names.get(e.revision_id) ?? "source"),
                            " ↗"
                        ]
                    }, `${e.span_id}-${e.stance}`, true, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 89,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 87,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
        lineNumber: 60,
        columnNumber: 5
    }, this);
}
_c1 = Row;
function CourseOfCareView({ patientId, runId, onSource }) {
    _s();
    const [record, setRecord] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [error, setError] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [group, setGroup] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("All");
    const [openOnly, setOpenOnly] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [query, setQuery] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const path = `/patients/${patientId}/analyses/${runId}/course-of-care`;
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "CourseOfCareView.useEffect": ()=>{
            let disposed = false;
            (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])(path).then({
                "CourseOfCareView.useEffect": (value)=>!disposed && setRecord(value)
            }["CourseOfCareView.useEffect"]).catch({
                "CourseOfCareView.useEffect": (reason)=>!disposed && setError(String(reason))
            }["CourseOfCareView.useEffect"]);
            return ({
                "CourseOfCareView.useEffect": ()=>{
                    disposed = true;
                }
            })["CourseOfCareView.useEffect"];
        }
    }["CourseOfCareView.useEffect"], [
        path
    ]);
    const visible = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMemo"])({
        "CourseOfCareView.useMemo[visible]": ()=>{
            if (!record) return [];
            const needle = query.trim().toLowerCase();
            return record.assertions.filter({
                "CourseOfCareView.useMemo[visible]": (a)=>GROUPS[group](a) && (!openOnly || OPEN.has(a.status) || a.status === "superseded") && (!needle || `${a.subject} ${a.text}`.toLowerCase().includes(needle))
            }["CourseOfCareView.useMemo[visible]"]);
        }
    }["CourseOfCareView.useMemo[visible]"], [
        record,
        group,
        openOnly,
        query
    ]);
    if (error) return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        className: "alert warning",
        children: error
    }, void 0, false, {
        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
        lineNumber: 141,
        columnNumber: 21
    }, this);
    if (!record) return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "empty small",
        children: "Loading course of care…"
    }, void 0, false, {
        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
        lineNumber: 143,
        columnNumber: 12
    }, this);
    const byDate = new Map();
    for (const a of visible){
        const key = a.valid_time.date ?? "Undated";
        byDate.set(key, [
            ...byDate.get(key) ?? [],
            a
        ]);
    }
    const open = record.assertions.filter((a)=>OPEN.has(a.status) && a.kind !== "finding");
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        className: "course-of-care",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "coc-heading",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                children: "Course of care"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                lineNumber: 158,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                children: [
                                    String(record.episode.first_date ?? ""),
                                    " –",
                                    " ",
                                    String(record.episode.last_date ?? ""),
                                    " ·",
                                    " ",
                                    record.assertions.length,
                                    " assertions from ",
                                    record.documents.length,
                                    " ",
                                    "documents · every assertion links to its source lines"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                lineNumber: 159,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 157,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        className: "text-action",
                        href: `/api/v1${path}?download=true`,
                        children: "Download JSON"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 166,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 156,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "coc-summary",
                children: Object.entries(record.summary).map(([status, count])=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Badge, {
                                status: status
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                lineNumber: 173,
                                columnNumber: 13
                            }, this),
                            " ",
                            count
                        ]
                    }, status, true, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 172,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 170,
                columnNumber: 7
            }, this),
            open.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "coc-open",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h4", {
                        children: "Open items — conflicting or not documented"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 180,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                        className: "assertion-list",
                        children: open.map((a)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Row, {
                                assertion: a,
                                record: record,
                                onSource: onSource
                            }, a.id, false, {
                                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                lineNumber: 183,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 181,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 179,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "coc-filters",
                children: [
                    Object.keys(GROUPS).map((name)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            className: group === name ? "active" : "",
                            onClick: ()=>setGroup(name),
                            children: name
                        }, name, false, {
                            fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                            lineNumber: 196,
                            columnNumber: 11
                        }, this)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                type: "checkbox",
                                checked: openOnly,
                                onChange: (event)=>setOpenOnly(event.target.checked)
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                lineNumber: 205,
                                columnNumber: 11
                            }, this),
                            " ",
                            "Only unresolved or superseded"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 204,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                        "aria-label": "Filter assertions",
                        placeholder: "Filter…",
                        value: query,
                        onChange: (event)=>setQuery(event.target.value)
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 212,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 194,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ol", {
                className: "coc-timeline",
                children: [
                    [
                        ...byDate.entries()
                    ].map(([day, items])=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h4", {
                                    children: day
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                    lineNumber: 223,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                                    className: "assertion-list",
                                    children: items.map((a)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(Row, {
                                            assertion: a,
                                            record: record,
                                            onSource: onSource
                                        }, a.id, false, {
                                            fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                            lineNumber: 226,
                                            columnNumber: 17
                                        }, this))
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                    lineNumber: 224,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, day, true, {
                            fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                            lineNumber: 222,
                            columnNumber: 11
                        }, this)),
                    !visible.length && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "empty small",
                        children: "No assertions match."
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 237,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 220,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                className: "coc-rules",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                        children: "Conflict-resolution rules"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 242,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dl", {
                        children: Object.entries(record.rules).map(([name, text])=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dt", {
                                        children: name.replaceAll("_", " ")
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                        lineNumber: 246,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("dd", {
                                        children: text
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                        lineNumber: 247,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, name, true, {
                                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                                lineNumber: 245,
                                columnNumber: 13
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                        lineNumber: 243,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/course-of-care-view.tsx",
                lineNumber: 241,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/course-of-care-view.tsx",
        lineNumber: 155,
        columnNumber: 5
    }, this);
}
_s(CourseOfCareView, "UtW772qIr9WKt4W0dmpeAvjIi+g=");
_c2 = CourseOfCareView;
var _c, _c1, _c2;
__turbopack_context__.k.register(_c, "Badge");
__turbopack_context__.k.register(_c1, "Row");
__turbopack_context__.k.register(_c2, "CourseOfCareView");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/app/document-timeline.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "DocumentTimeline",
    ()=>DocumentTimeline
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/evidence-views.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
const whenLabel = (when)=>`${when.date}${when.end_date ? ` – ${when.end_date}` : ""}${when.time ? ` · ${when.time}` : ""}${when.timezone ? ` (${when.timezone})` : when.time ? " (timezone not stated)" : ""}`;
function DocumentTimeline({ run, patientId, onSource }) {
    _s();
    const [axis, setAxis] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("history");
    const [filter, setFilter] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const catalog = run.result?.document_catalog;
    if (!catalog) return null;
    const sources = run.result?.document_sources ?? [];
    const citations = run.result?.citations ?? [];
    const sourceFor = (doc)=>sources.find((s)=>s.revision_id === doc.revision_id);
    const docs = catalog.documents.filter((doc)=>[
            doc.title,
            sourceFor(doc)?.filename,
            doc.document_type,
            ...doc.contributors.map((p)=>p.name),
            ...doc.signatures.map((s)=>s.name)
        ].join(" ").toLowerCase().includes(filter.toLowerCase()));
    const rows = docs.flatMap((doc)=>{
        const events = axis === "ingestion" ? [] : doc.dates.filter((event)=>axis === "service" ? [
                "service",
                "measurement",
                "effective"
            ].includes(event.kind) : ![
                "service",
                "measurement",
                "effective"
            ].includes(event.kind)).map((event)=>({
                label: `${(0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(event.kind)} · ${event.scope}`,
                when: event.when,
                citations: event.citations
            }));
        if (axis === "history") {
            for (const signature of doc.signatures){
                if (signature.when) events.push({
                    label: `${(0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(signature.kind)} · ${signature.name}`,
                    when: signature.when,
                    citations: signature.citations
                });
            }
        }
        if (axis === "ingestion") {
            const rawIngested = sourceFor(doc)?.ingested_at;
            const ingested = rawIngested ? new Date(rawIngested).toISOString() : undefined;
            return [
                {
                    doc,
                    sort: ingested ?? "9999",
                    label: "Imported into this workspace",
                    date: ingested ? `${ingested.slice(0, 10)} · ${ingested.slice(11, 19)} UTC` : "Import date unavailable",
                    citations: []
                }
            ];
        }
        if (!events.length) return [
            {
                doc,
                sort: "9999",
                label: axis === "service" ? "Service date not established" : "Document history date not established",
                date: "Undated",
                citations: []
            }
        ];
        return events.map((event)=>({
                doc,
                sort: `${event.when.date}T${event.when.time ?? ""}`,
                label: event.label,
                date: whenLabel(event.when),
                citations: event.citations
            }));
    }).sort((a, b)=>a.sort.localeCompare(b.sort) || a.doc.title.localeCompare(b.doc.title));
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "draft-notice",
                children: [
                    "Unreviewed document metadata · ",
                    catalog.documents.length,
                    " sources. Signatures are reported from the text, not authenticated. Repeated entries represent document history, not additional visits."
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/document-timeline.tsx",
                lineNumber: 117,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "timeline-controls",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            "Timeline dates",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                "aria-label": "Timeline dates",
                                value: axis,
                                onChange: (e)=>setAxis(e.target.value),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: "history",
                                        children: "Document history"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 130,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: "service",
                                        children: "Clinical and effective dates"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 131,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: "ingestion",
                                        children: "Workspace import dates"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 132,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                lineNumber: 125,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                        lineNumber: 123,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            "Find a document",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                "aria-label": "Find a document",
                                placeholder: "Title, filename, author or signer",
                                value: filter,
                                onChange: (e)=>setFilter(e.target.value)
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                lineNumber: 137,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                        lineNumber: 135,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/document-timeline.tsx",
                lineNumber: 122,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "muted-text",
                children: axis === "history" ? "Creation, entry, review, signature, receipt, posting and export dates. Dates without a stated time have no inferred order within that day." : axis === "service" ? "Service, questionnaire completion and plan effective dates. These do not all represent attended visits. One document may cover several dates." : "When each source revision first entered this workspace, from system records. These are not clinical or signature dates."
            }, void 0, false, {
                fileName: "[project]/apps/web/app/document-timeline.tsx",
                lineNumber: 145,
                columnNumber: 7
            }, this),
            !rows.length && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                children: "No matching documents."
            }, void 0, false, {
                fileName: "[project]/apps/web/app/document-timeline.tsx",
                lineNumber: 152,
                columnNumber: 24
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ol", {
                className: "document-timeline",
                children: rows.map((row, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "timeline-date",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: row.date
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 157,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: row.label
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 158,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                lineNumber: 156,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                className: "document-card",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "eyebrow",
                                        children: [
                                            (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(row.doc.document_type),
                                            " ·",
                                            " ",
                                            row.doc.stated_status ?? "Record status unknown"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 161,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>onSource(row.doc.revision_id, row.citations[0] ?? row.doc.citations[0] ?? ""),
                                            children: [
                                                row.doc.title,
                                                " ↗"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/apps/web/app/document-timeline.tsx",
                                            lineNumber: 166,
                                            columnNumber: 17
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 165,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "document-filename",
                                        children: sourceFor(row.doc)?.filename
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 177,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                        className: "document-evidence",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                children: [
                                                    "Document details · signatures",
                                                    " ",
                                                    (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(row.doc.signature_status)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                lineNumber: 181,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                children: [
                                                    "Authors:",
                                                    " ",
                                                    row.doc.contributors.filter((p)=>p.role === "author").map((p)=>p.name).join("; ") || "Not established"
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                lineNumber: 185,
                                                columnNumber: 17
                                            }, this),
                                            row.doc.contributors.some((person)=>person.role !== "author") && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                children: row.doc.contributors.filter((person)=>person.role !== "author").map((person)=>`${(0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(person.role)}: ${person.name}`).join("; ")
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                lineNumber: 195,
                                                columnNumber: 19
                                            }, this),
                                            (row.doc.statuses ?? []).map((status, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    children: [
                                                        status.scope,
                                                        ": ",
                                                        status.value
                                                    ]
                                                }, `status-${i}`, true, {
                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                    lineNumber: 203,
                                                    columnNumber: 19
                                                }, this)),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                children: [
                                                    "Signature status: ",
                                                    (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(row.doc.signature_status),
                                                    row.doc.signatures.length > 0 && ` · ${row.doc.signatures.map((s)=>`${s.name} (${(0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(s.kind)})`).join("; ")}`
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                lineNumber: 207,
                                                columnNumber: 17
                                            }, this),
                                            row.doc.relations.map((rel, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "document-relation",
                                                    children: [
                                                        (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(rel.kind),
                                                        ": ",
                                                        rel.target_description,
                                                        " · ",
                                                        rel.scope,
                                                        rel.target_revision_id && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                                            children: [
                                                                " ",
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                                    onClick: ()=>onSource(rel.target_revision_id, ""),
                                                                    children: "Open related source ↗"
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 218,
                                                                    columnNumber: 25
                                                                }, this)
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                            lineNumber: 216,
                                                            columnNumber: 23
                                                        }, this)
                                                    ]
                                                }, i, true, {
                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                    lineNumber: 213,
                                                    columnNumber: 19
                                                }, this)),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                                className: "document-evidence",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                        children: "People, dates and supporting evidence"
                                                    }, void 0, false, {
                                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                        lineNumber: 228,
                                                        columnNumber: 19
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                        ids: row.doc.citations,
                                                        citations: citations,
                                                        onSource: onSource
                                                    }, void 0, false, {
                                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                        lineNumber: 229,
                                                        columnNumber: 19
                                                    }, this),
                                                    (row.doc.statuses ?? []).map((status, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                    children: [
                                                                        status.scope,
                                                                        ": ",
                                                                        status.value
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 236,
                                                                    columnNumber: 23
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                                    ids: status.citations,
                                                                    citations: citations,
                                                                    onSource: onSource
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 239,
                                                                    columnNumber: 23
                                                                }, this)
                                                            ]
                                                        }, `status-${i}`, true, {
                                                            fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                            lineNumber: 235,
                                                            columnNumber: 21
                                                        }, this)),
                                                    row.doc.contributors.map((person, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                    children: [
                                                                        (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(person.role),
                                                                        ": ",
                                                                        person.name,
                                                                        " · ",
                                                                        person.scope
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 248,
                                                                    columnNumber: 23
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                                    ids: person.citations,
                                                                    citations: citations,
                                                                    onSource: onSource
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 251,
                                                                    columnNumber: 23
                                                                }, this)
                                                            ]
                                                        }, `person-${i}`, true, {
                                                            fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                            lineNumber: 247,
                                                            columnNumber: 21
                                                        }, this)),
                                                    row.doc.signatures.map((signature, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                    children: [
                                                                        (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(signature.kind),
                                                                        ": ",
                                                                        signature.name,
                                                                        " ·",
                                                                        " ",
                                                                        signature.scope,
                                                                        " ·",
                                                                        " ",
                                                                        signature.when ? whenLabel(signature.when) : "Date not stated"
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 260,
                                                                    columnNumber: 23
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                                    ids: signature.citations,
                                                                    citations: citations,
                                                                    onSource: onSource
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 267,
                                                                    columnNumber: 23
                                                                }, this)
                                                            ]
                                                        }, `signature-${i}`, true, {
                                                            fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                            lineNumber: 259,
                                                            columnNumber: 21
                                                        }, this)),
                                                    row.doc.dates.map((event, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                    children: [
                                                                        (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(event.kind),
                                                                        ": ",
                                                                        whenLabel(event.when),
                                                                        " ·",
                                                                        " ",
                                                                        event.scope
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 276,
                                                                    columnNumber: 23
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                                    ids: event.citations,
                                                                    citations: citations,
                                                                    onSource: onSource
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 280,
                                                                    columnNumber: 23
                                                                }, this)
                                                            ]
                                                        }, `date-${i}`, true, {
                                                            fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                            lineNumber: 275,
                                                            columnNumber: 21
                                                        }, this)),
                                                    row.doc.relations.map((rel, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                    children: [
                                                                        "Source-described relationship: ",
                                                                        (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["human"])(rel.kind),
                                                                        " ·",
                                                                        " ",
                                                                        rel.scope
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 289,
                                                                    columnNumber: 23
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
                                                                    ids: rel.citations,
                                                                    citations: citations,
                                                                    onSource: onSource
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                                    lineNumber: 293,
                                                                    columnNumber: 23
                                                                }, this)
                                                            ]
                                                        }, `relation-${i}`, true, {
                                                            fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                            lineNumber: 288,
                                                            columnNumber: 21
                                                        }, this))
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                                lineNumber: 227,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                                        lineNumber: 180,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/document-timeline.tsx",
                                lineNumber: 160,
                                columnNumber: 13
                            }, this)
                        ]
                    }, `${row.doc.revision_id}-${index}`, true, {
                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                        lineNumber: 155,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/apps/web/app/document-timeline.tsx",
                lineNumber: 153,
                columnNumber: 7
            }, this),
            catalog.limitations.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                className: "coverage-details",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                        children: "Metadata gaps and limitations"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                        lineNumber: 308,
                        columnNumber: 11
                    }, this),
                    catalog.limitations.map((value, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            children: value
                        }, i, false, {
                            fileName: "[project]/apps/web/app/document-timeline.tsx",
                            lineNumber: 310,
                            columnNumber: 13
                        }, this))
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/document-timeline.tsx",
                lineNumber: 307,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                className: "coverage-details",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                        children: "Inspect document JSON"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                        lineNumber: 315,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "abstraction-json",
                        children: JSON.stringify({
                            scope: {
                                patient_id: patientId,
                                snapshot_id: run.snapshot_id
                            },
                            extraction: {
                                run_id: run.id,
                                schema_version: run.schema_version,
                                prompt_version: run.prompt_version,
                                model: run.model,
                                created_at: run.created_at,
                                review_status: "unreviewed"
                            },
                            ...catalog,
                            sources,
                            citations
                        }, null, 2)
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/document-timeline.tsx",
                        lineNumber: 316,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/document-timeline.tsx",
                lineNumber: 314,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/document-timeline.tsx",
        lineNumber: 116,
        columnNumber: 5
    }, this);
}
_s(DocumentTimeline, "ogmdn7GvMqjQMJpEbwiBZ0G6m30=");
_c = DocumentTimeline;
var _c;
__turbopack_context__.k.register(_c, "DocumentTimeline");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/app/evidence-views.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Calculated",
    ()=>Calculated,
    "Findings",
    ()=>Findings,
    "References",
    ()=>References,
    "human",
    ()=>human,
    "minutes",
    ()=>minutes,
    "sourceLabel",
    ()=>sourceLabel
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
"use client";
;
const minutes = (seconds)=>seconds.length ? seconds.map((value)=>`${value / 60}`).join(" or ") + " min" : "Unknown";
const human = (value)=>value === "claude_credit_balance_low" ? "Anthropic credits are exhausted. Add credits to your Anthropic account, then retry." : value === "answer_requires_review" ? "The answer did not pass its source check, so it was not published." : value === "abstraction_requires_review" ? "No source-checked abstraction is ready. Retry the flagged documents." : value.replaceAll("_", " ");
const sourceLabel = (filename)=>{
    const label = filename.replace(/\.[a-z]+$/i, "").replaceAll("_", " ");
    return label.length > 48 ? `${label.slice(0, 47)}…` : label;
};
function References({ ids, citations, onSource }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "evidence-links",
        children: [
            ...new Set(ids)
        ].map((id)=>{
            const citation = citations.find((value)=>value.span_id === id);
            return citation ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                title: citation.quote,
                onClick: ()=>onSource(citation.revision_id, id),
                children: [
                    sourceLabel(citation.filename),
                    " · L",
                    citation.start_line,
                    "–",
                    citation.end_line,
                    " ↗"
                ]
            }, id, true, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 39,
                columnNumber: 11
            }, this) : null;
        })
    }, void 0, false, {
        fileName: "[project]/apps/web/app/evidence-views.tsx",
        lineNumber: 35,
        columnNumber: 5
    }, this);
}
_c = References;
function Findings({ claims, citations, onSource }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "clinical-findings",
        children: claims.map((claim, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                className: "finding",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "eyebrow",
                        children: claim.category
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 66,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        children: claim.text
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 67,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(References, {
                        ids: claim.citations,
                        citations: citations,
                        onSource: onSource
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 68,
                        columnNumber: 11
                    }, this)
                ]
            }, index, true, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 65,
                columnNumber: 9
            }, this))
    }, void 0, false, {
        fileName: "[project]/apps/web/app/evidence-views.tsx",
        lineNumber: 63,
        columnNumber: 5
    }, this);
}
_c1 = Findings;
function Calculated({ value, citations, onSource }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        className: "calculation",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "section-title",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                        children: "Calculated from the encounter ledger"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 91,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "verified",
                        children: "Server calculation"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 92,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 90,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "muted-text",
                children: [
                    value.total.start,
                    " – ",
                    value.total.end,
                    " · Included encounters of the services the documented goal counts"
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 94,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "summary-grid",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "summary",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Sessions"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 100,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                children: value.total.sessions ?? "Unknown"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 101,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 99,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "summary",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Distinct treatment days"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 104,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                children: value.total.days ?? "Unknown"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 105,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 103,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "summary",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Patient treatment time"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 108,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                children: minutes(value.total.seconds)
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 109,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 107,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 98,
                columnNumber: 7
            }, this),
            !value.total.complete && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "alert warning",
                children: "Coverage, attendance, or duration is unresolved. A definitive total is withheld."
            }, void 0, false, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 113,
                columnNumber: 9
            }, this),
            (value.total.by_modality ?? []).length > 1 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("table", {
                className: "breakdown",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("caption", {
                        children: "By service type"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 120,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("thead", {
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    children: "Service"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 123,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    children: "Sessions"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 124,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    children: "Days"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 125,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    children: "Time"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 126,
                                    columnNumber: 15
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/apps/web/app/evidence-views.tsx",
                            lineNumber: 122,
                            columnNumber: 13
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 121,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tbody", {
                        children: (value.total.by_modality ?? []).map((row)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                        scope: "row",
                                        children: row.modality
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 132,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                        children: row.sessions ?? "Unknown"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 133,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                        children: row.days ?? "Unknown"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 134,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                        children: minutes(row.seconds)
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 135,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, row.modality, true, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 131,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 129,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 119,
                columnNumber: 9
            }, this),
            (value.periods ?? []).length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("table", {
                className: "breakdown",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("caption", {
                        children: "By period"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 143,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("thead", {
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    children: "Period"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 146,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    children: "Sessions"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 147,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    children: "Days"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 148,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                    scope: "col",
                                    children: "Time"
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 149,
                                    columnNumber: 15
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/apps/web/app/evidence-views.tsx",
                            lineNumber: 145,
                            columnNumber: 13
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 144,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tbody", {
                        children: (value.periods ?? []).map((row)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                        scope: "row",
                                        children: [
                                            row.start,
                                            " – ",
                                            row.end
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 155,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                        children: row.sessions ?? "Unknown"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 158,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                        children: row.days ?? "Unknown"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 159,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                        children: minutes(row.seconds)
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 160,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, `${row.start}-${row.end}`, true, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 154,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 152,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 142,
                columnNumber: 9
            }, this),
            value.weeks.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "weekly-grid",
                children: value.weeks.map((week, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                        className: "week-card",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                children: [
                                    week.start,
                                    " – ",
                                    week.end
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 170,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: [
                                    week.days ?? "Unknown",
                                    " days · ",
                                    minutes(week.seconds)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 173,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: `disposition ${week.goal_status}`,
                                children: human(week.goal_status)
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 176,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                children: [
                                    "Goal: ",
                                    week.minimum_days,
                                    " days AND ",
                                    week.minimum_minutes,
                                    " min"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 179,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(References, {
                                ids: week.citations,
                                citations: citations,
                                onSource: onSource
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/evidence-views.tsx",
                                lineNumber: 182,
                                columnNumber: 15
                            }, this)
                        ]
                    }, index, true, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 169,
                        columnNumber: 13
                    }, this))
            }, void 0, false, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 167,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                className: "calculation-details",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                        children: "Show contributions and calculation assumptions"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                        lineNumber: 192,
                        columnNumber: 9
                    }, this),
                    value.contributions.map((row)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "contribution",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    children: [
                                        row.date,
                                        " · ",
                                        row.encounter_id,
                                        " · ",
                                        row.modality
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 195,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                    children: row.disposition === "excluded" ? "Excluded" : row.disposition === "uncertain" ? "Uncertain" : minutes(row.seconds)
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 198,
                                    columnNumber: 13
                                }, this),
                                (row.accounts ?? []).filter((account)=>account.present_seconds !== null).map((account, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                        children: [
                                            "Present ",
                                            Math.round((account.present_seconds ?? 0) / 60),
                                            " min − nontherapeutic",
                                            " ",
                                            Math.round((account.break_seconds ?? 0) / 60),
                                            " min =",
                                            " ",
                                            Math.round(account.therapy_seconds / 60),
                                            " min"
                                        ]
                                    }, index, true, {
                                        fileName: "[project]/apps/web/app/evidence-views.tsx",
                                        lineNumber: 208,
                                        columnNumber: 17
                                    }, this)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(References, {
                                    ids: row.citations,
                                    citations: citations,
                                    onSource: onSource
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/evidence-views.tsx",
                                    lineNumber: 215,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, row.encounter_id, true, {
                            fileName: "[project]/apps/web/app/evidence-views.tsx",
                            lineNumber: 194,
                            columnNumber: 11
                        }, this)),
                    value.notes.map((note)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            children: note
                        }, note, false, {
                            fileName: "[project]/apps/web/app/evidence-views.tsx",
                            lineNumber: 223,
                            columnNumber: 11
                        }, this))
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/evidence-views.tsx",
                lineNumber: 191,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/evidence-views.tsx",
        lineNumber: 89,
        columnNumber: 5
    }, this);
}
_c2 = Calculated;
var _c, _c1, _c2;
__turbopack_context__.k.register(_c, "References");
__turbopack_context__.k.register(_c1, "Findings");
__turbopack_context__.k.register(_c2, "Calculated");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/app/import-panel.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ImportPanel",
    ()=>ImportPanel
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
"use client";
;
function ImportPanel({ files, busy, onFiles, onImport }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                className: "panel import-panel",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "import-icon",
                        children: "↥"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/import-panel.tsx",
                        lineNumber: 17,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                children: "Upload your records"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/import-panel.tsx",
                                lineNumber: 19,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                children: "We detect the patient and group matching records automatically."
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/import-panel.tsx",
                                lineNumber: 20,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                children: "UTF-8 TXT · 10 MiB per file · 25 MiB per import · 100 files"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/import-panel.tsx",
                                lineNumber: 21,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/import-panel.tsx",
                        lineNumber: 18,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        className: "secondary file-button",
                        children: [
                            "Choose files",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                "aria-label": "Choose source files",
                                type: "file",
                                accept: ".txt,text/plain",
                                multiple: true,
                                disabled: busy,
                                onChange: (event)=>{
                                    onFiles(Array.from(event.target.files ?? []));
                                    event.target.value = "";
                                }
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/import-panel.tsx",
                                lineNumber: 25,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/import-panel.tsx",
                        lineNumber: 23,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: "primary",
                        disabled: !files.length || busy,
                        onClick: onImport,
                        children: busy ? "Importing…" : files.length ? `Import ${files.length} file${files.length > 1 ? "s" : ""}` : "Import records"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/import-panel.tsx",
                        lineNumber: 37,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/import-panel.tsx",
                lineNumber: 16,
                columnNumber: 7
            }, this),
            files.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "file-preview",
                children: [
                    "Ready to import: ",
                    files.map((file)=>file.name).join(", ")
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/import-panel.tsx",
                lineNumber: 50,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/import-panel.tsx",
        lineNumber: 15,
        columnNumber: 5
    }, this);
}
_c = ImportPanel;
var _c;
__turbopack_context__.k.register(_c, "ImportPanel");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/app/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Workspace
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/lib/api.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$import$2d$panel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/import-panel.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$clinical$2d$panel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/clinical-panel.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
;
const message = (error)=>error instanceof Error ? error.message : "Something went wrong.";
function Workspace() {
    _s();
    const [view, setView] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("sources");
    const [session, setSession] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [starting, setStarting] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(true);
    const [patients, setPatients] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [patient, setPatient] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [documents, setDocuments] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [jobs, setJobs] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [snapshots, setSnapshots] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [snapshotId, setSnapshotId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [source, setSource] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [spanId, setSpanId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [query, setQuery] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [files, setFiles] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [busy, setBusy] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [loadingSource, setLoadingSource] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [error, setError] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [batches, setBatches] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [importNotice, setImportNotice] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [removing, setRemoving] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [removeReason, setRemoveReason] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const patientRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    const sourceRequest = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(0);
    const retryImport = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    const loadPatients = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "Workspace.useCallback[loadPatients]": async ()=>{
            const [values, imports] = await Promise.all([
                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["allPages"])("/patients"),
                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["allPages"])("/imports")
            ]);
            setBatches(imports);
            setPatients(values);
            const requestedId = new URL(window.location.href).searchParams.get("patient");
            // Never silently switch a bookmarked patient to a different chart.
            setPatient({
                "Workspace.useCallback[loadPatients]": (current)=>current ?? (requestedId ? values.find({
                        "Workspace.useCallback[loadPatients]": (value)=>value.id === requestedId
                    }["Workspace.useCallback[loadPatients]"]) ?? null : values.length === 1 ? values[0] : null)
            }["Workspace.useCallback[loadPatients]"]);
            return values;
        }
    }["Workspace.useCallback[loadPatients]"], []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "Workspace.useEffect": ()=>{
            (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])("/session").then({
                "Workspace.useEffect": async (value)=>{
                    setSession(value);
                    await loadPatients();
                }
            }["Workspace.useEffect"]).catch({
                "Workspace.useEffect": (error)=>{
                    if (!message(error).startsWith("401")) setError(message(error));
                }
            }["Workspace.useEffect"]).finally({
                "Workspace.useEffect": ()=>setStarting(false)
            }["Workspace.useEffect"]);
        }
    }["Workspace.useEffect"], [
        loadPatients
    ]);
    const refresh = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "Workspace.useCallback[refresh]": async (id)=>{
            const [docs, imports, versions] = await Promise.all([
                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["allPages"])(`/patients/${id}/documents`),
                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["allPages"])(`/patients/${id}/jobs`),
                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])(`/patients/${id}/snapshots`)
            ]);
            if (patientRef.current !== id) return;
            setDocuments(docs);
            setJobs(imports);
            setSnapshots(versions);
        }
    }["Workspace.useCallback[refresh]"], []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "Workspace.useEffect": ()=>{
            patientRef.current = patient?.id ?? null;
            sourceRequest.current += 1;
            setSource(null);
            setDocuments([]);
            setJobs([]);
            setSnapshots([]);
            setSnapshotId("");
            setLoadingSource(false);
            setSpanId("");
            if (!patient) return;
            const url = new URL(window.location.href);
            url.searchParams.set("patient", patient.id);
            window.history.replaceState(null, "", url);
            let disposed = false;
            let timer;
            const poll = {
                "Workspace.useEffect.poll": async ()=>{
                    try {
                        await refresh(patient.id);
                    } catch (error) {
                        if (!disposed) setError(message(error));
                    }
                    if (!disposed) timer = setTimeout(poll, 2000);
                }
            }["Workspace.useEffect.poll"];
            void poll();
            return ({
                "Workspace.useEffect": ()=>{
                    disposed = true;
                    clearTimeout(timer);
                }
            })["Workspace.useEffect"];
        }
    }["Workspace.useEffect"], [
        patient,
        refresh
    ]);
    async function signIn() {
        setBusy(true);
        setError("");
        try {
            setSession(await (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])("/dev-session", {
                method: "POST"
            }));
            await loadPatients();
        } catch (error) {
            setError(message(error));
        } finally{
            setBusy(false);
        }
    }
    async function upload() {
        if (!session || !files.length) return;
        setBusy(true);
        setError("");
        const form = new FormData();
        files.forEach((file)=>form.append("files", file));
        const signature = JSON.stringify([
            files.map((file)=>[
                    file.name,
                    file.size,
                    file.lastModified
                ])
        ]);
        if (retryImport.current?.signature !== signature) retryImport.current = {
            signature,
            key: crypto.randomUUID()
        };
        try {
            const result = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])("/imports", {
                method: "POST",
                headers: {
                    "X-CSRF-Token": session.csrf_token,
                    "Idempotency-Key": retryImport.current.key
                },
                body: form
            });
            retryImport.current = null;
            setFiles([]);
            const values = await loadPatients();
            const ids = new Set(result.jobs.map((job)=>job.patient_id));
            if (ids.size === 1) {
                const next = values.find((value)=>ids.has(value.id)) ?? null;
                setPatient(next);
                if (next && patientRef.current === next.id) await refresh(next.id);
            } else if (ids.size > 1) {
                setPatient(null);
                const url = new URL(window.location.href);
                url.searchParams.delete("patient");
                window.history.replaceState(null, "", url);
            }
            setImportNotice(ids.size > 1 ? `${ids.size} patients detected. Records were grouped separately; choose a patient to inspect their sources.` : ids.size === 1 ? "Patient detected. Your records are being processed in the matching case." : "These files need identity review before they can be attached to a patient.");
        } catch (error) {
            setError(message(error));
        } finally{
            setBusy(false);
        }
    }
    async function openSource(id, targetSpan = "") {
        const request = ++sourceRequest.current;
        setLoadingSource(true);
        setError("");
        try {
            const next = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])(`/source-revisions/${id}`);
            if (sourceRequest.current === request) {
                setSource(next);
                setSpanId(targetSpan);
            }
        } catch (error) {
            if (sourceRequest.current === request) setError(message(error));
        } finally{
            if (sourceRequest.current === request) setLoadingSource(false);
        }
    }
    async function changeDocument(id, action, reason) {
        if (!session || !patient) return;
        setBusy(true);
        setError("");
        try {
            await (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])(`/patients/${patient.id}/documents/${id}/${action}`, {
                method: "POST",
                headers: {
                    "X-CSRF-Token": session.csrf_token,
                    "Content-Type": "application/json"
                },
                body: action === "withdraw" ? JSON.stringify({
                    reason
                }) : undefined
            });
            setRemoving(false);
            setRemoveReason("");
            setSnapshotId("");
            if (action === "withdraw") setSource(null);
            await refresh(patient.id);
        } catch (error) {
            setError(message(error));
        } finally{
            setBusy(false);
        }
    }
    const selectedSnapshot = snapshots.find((value)=>value.id === snapshotId) ?? snapshots[0];
    const included = new Set(selectedSnapshot?.manifest.map((value)=>value.revision_id));
    const visibleDocs = documents.filter((doc)=>(!selectedSnapshot || included.has(doc.id)) && `${doc.filename} ${doc.declared_id ?? ""}`.toLowerCase().includes(query.toLowerCase()));
    const withdrawnDocs = documents.filter((doc)=>doc.withdrawn);
    const viewingLatest = !snapshotId || snapshotId === snapshots[0]?.id;
    const sourceWithdrawn = documents.some((doc)=>doc.id === source?.id && doc.withdrawn);
    const activeJobs = jobs.filter((job)=>[
            "queued",
            "running"
        ].includes(job.status));
    const issues = jobs.flatMap((job)=>job.uploads.filter((upload)=>[
                "quarantined",
                "failed"
            ].includes(upload.status)));
    const highlighted = source?.spans.find((span)=>span.id === spanId);
    const lines = source?.text.split(/\r\n|[\n\r\v\f\x85\u2028\u2029]/) ?? [];
    if (lines.at(-1) === "") lines.pop();
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "shell",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("aside", {
                className: "sidebar",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        className: "brand",
                        href: "/",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "brand-icon",
                                children: "e"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 267,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: [
                                    "Evidence",
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "brand-sub",
                                        children: "CLINICAL WORKSPACE"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 269,
                                        columnNumber: 21
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 268,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 266,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "nav-label",
                        children: "WORKSPACE"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 272,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: `nav-item ${view === "sources" ? "active" : ""}`,
                        onClick: ()=>setView("sources"),
                        "aria-label": "Source library",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "▤"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 278,
                                columnNumber: 11
                            }, this),
                            " Source library"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 273,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: `nav-item ${view === "abstraction" ? "active" : ""}`,
                        onClick: ()=>setView("abstraction"),
                        "aria-label": "Abstraction",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "◷"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 285,
                                columnNumber: 11
                            }, this),
                            " Abstraction"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 280,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: `nav-item ${view === "documents" ? "active" : ""}`,
                        onClick: ()=>setView("documents"),
                        "aria-label": "Document timeline",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "≡"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 292,
                                columnNumber: 11
                            }, this),
                            " Document timeline"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 287,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: `nav-item ${view === "ask" ? "active" : ""}`,
                        onClick: ()=>setView("ask"),
                        "aria-label": "Ask a question",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "◇"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 299,
                                columnNumber: 11
                            }, this),
                            " Ask a question"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 294,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "sidebar-bottom",
                        children: [
                            "Development workspace",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                children: "Synthetic records only."
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 303,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 301,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/page.tsx",
                lineNumber: 265,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
                        className: "topbar",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: [
                                    "Records ",
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "slash",
                                        children: "/"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 309,
                                        columnNumber: 21
                                    }, this),
                                    " ",
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: view === "sources" ? "Source library" : view === "abstraction" ? "Abstraction" : view === "documents" ? "Document timeline" : "Ask a question"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 310,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 308,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "development",
                                children: "LOCAL DEVELOPMENT"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 320,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 307,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "content",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "page-heading",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                                        children: view === "sources" ? "Every source. In context." : view === "abstraction" ? "From records to a clear picture." : view === "documents" ? "The history behind the record." : "Answers with evidence."
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 324,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        children: "Import records, inspect sources, and ask questions."
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 333,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 323,
                                columnNumber: 11
                            }, this),
                            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                role: "alert",
                                className: "alert error",
                                children: error
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 336,
                                columnNumber: 13
                            }, this),
                            starting ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                role: "status",
                                className: "empty",
                                children: "Opening your workspace…"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 341,
                                columnNumber: 13
                            }, this) : !session ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                                className: "welcome panel",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "empty-icon",
                                        children: "▤"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 346,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                        children: "A clear view of your source records"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 347,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        children: "Upload fictional patient records. We identify the patient and group their documents, with exact, stable source citations."
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 348,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "primary",
                                        disabled: busy,
                                        onClick: signIn,
                                        children: busy ? "Opening…" : "Enter development workspace →"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 352,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                        children: "Development sign-in is shared. Production authentication is not enabled."
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 355,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 345,
                                columnNumber: 13
                            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                children: [
                                    view === "sources" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$import$2d$panel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ImportPanel"], {
                                        files: files,
                                        busy: busy,
                                        onFiles: (values)=>{
                                            setFiles(values);
                                            retryImport.current = null;
                                            setImportNotice("");
                                        },
                                        onImport: ()=>void upload()
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 363,
                                        columnNumber: 17
                                    }, this),
                                    importNotice && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "alert",
                                        role: "status",
                                        children: importNotice
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 375,
                                        columnNumber: 17
                                    }, this),
                                    batches.some((batch)=>batch.issues.length > 0) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                        className: "alert warning",
                                        open: true,
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                children: "Files awaiting identity review"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 381,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                children: "These files are saved separately and have not been attached to a patient."
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 382,
                                                columnNumber: 19
                                            }, this),
                                            batches.flatMap((batch)=>batch.issues).map((issue)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                            children: issue.filename
                                                        }, void 0, false, {
                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                            lineNumber: 390,
                                                            columnNumber: 25
                                                        }, this),
                                                        ":",
                                                        " ",
                                                        issue.error_code === "conflicting_identifiers" ? "Conflicting MRN or birth-date information. Review the source header before importing a corrected record." : issue.error_code === "identity_unconfirmed" ? "The record needs an explicit MRN and date of birth." : issue.error_code.replaceAll("_", " ")
                                                    ]
                                                }, issue.id, true, {
                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                    lineNumber: 389,
                                                    columnNumber: 23
                                                }, this))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 380,
                                        columnNumber: 17
                                    }, this),
                                    (patient || patients.length > 1) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                                        className: "patient-bar panel",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "patient-avatar",
                                                children: patient?.name.split(" ").map((part)=>part[0]).slice(0, 2).join("") || "▤"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 402,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "patient-picker",
                                                children: [
                                                    patients.length > 1 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                htmlFor: "patient",
                                                                children: "PATIENT"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 412,
                                                                columnNumber: 25
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                                                id: "patient",
                                                                value: patient?.id ?? "",
                                                                disabled: busy,
                                                                onChange: (event)=>setPatient(patients.find((value)=>value.id === event.target.value) ?? null),
                                                                children: [
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                                        value: "",
                                                                        disabled: true,
                                                                        children: "Select a patient"
                                                                    }, void 0, false, {
                                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                                        lineNumber: 425,
                                                                        columnNumber: 27
                                                                    }, this),
                                                                    patients.map((value)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                                            value: value.id,
                                                                            children: [
                                                                                value.name,
                                                                                " · ",
                                                                                value.mrn
                                                                            ]
                                                                        }, value.id, true, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 429,
                                                                            columnNumber: 29
                                                                        }, this))
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 413,
                                                                columnNumber: 25
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 411,
                                                        columnNumber: 23
                                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "eyebrow",
                                                                children: "PATIENT DETECTED"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 437,
                                                                columnNumber: 25
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                                children: patient?.name
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 438,
                                                                columnNumber: 25
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 436,
                                                        columnNumber: 23
                                                    }, this),
                                                    patient && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                                        children: [
                                                            "MRN ",
                                                            patient.mrn,
                                                            " ",
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                children: "·"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 443,
                                                                columnNumber: 43
                                                            }, this),
                                                            " DOB",
                                                            " ",
                                                            patient.birth_date
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 442,
                                                        columnNumber: 23
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 409,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 401,
                                        columnNumber: 17
                                    }, this),
                                    patient && view !== "sources" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$clinical$2d$panel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ClinicalPanel"], {
                                        patientId: patient.id,
                                        csrf: session.csrf_token,
                                        snapshot: selectedSnapshot,
                                        snapshots: snapshots,
                                        onSnapshot: setSnapshotId,
                                        view: view,
                                        onSource: (revision, span)=>{
                                            setView("sources");
                                            void openSource(revision, span);
                                        }
                                    }, patient.id, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 451,
                                        columnNumber: 17
                                    }, this),
                                    !patient && view !== "sources" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "empty",
                                        children: "Select a patient with imported records to view their abstraction and ask questions."
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 466,
                                        columnNumber: 17
                                    }, this),
                                    patient && view === "sources" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "summary-grid",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "panel summary",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                children: "Source documents"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 475,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                                children: selectedSnapshot?.manifest.length ?? 0
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 476,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                                                children: "Immutable text revisions"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 477,
                                                                columnNumber: 23
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 474,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "panel summary",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                children: "Import activity"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 480,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                                children: activeJobs.length ? `${activeJobs.length} active` : "Up to date"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 481,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                                                children: [
                                                                    jobs.length,
                                                                    " import",
                                                                    jobs.length !== 1 ? "s" : "",
                                                                    " in this workspace"
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 486,
                                                                columnNumber: 23
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 479,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "panel summary",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                children: "Clinical abstraction"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 492,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                                className: "text-action",
                                                                onClick: ()=>setView("abstraction"),
                                                                children: "Open abstraction →"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 493,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                                                children: "Claude extraction with source evidence"
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 499,
                                                                columnNumber: 23
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 491,
                                                        columnNumber: 21
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 473,
                                                columnNumber: 19
                                            }, this),
                                            activeJobs.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "alert",
                                                role: "status",
                                                children: "Processing source records. You can close this page and return later."
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 503,
                                                columnNumber: 21
                                            }, this),
                                            issues.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                                className: "alert warning",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                        children: [
                                                            issues.length,
                                                            " file",
                                                            issues.length !== 1 ? "s need" : " needs",
                                                            " attention · source coverage is incomplete"
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 510,
                                                        columnNumber: 23
                                                    }, this),
                                                    issues.map((issue)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            children: [
                                                                issue.filename,
                                                                ":",
                                                                " ",
                                                                issue.error_code === "identity_mismatch" ? `The file’s MRN or date of birth does not match ${patient.name} (${patient.mrn}, ${patient.birth_date}). Choose the matching patient workspace and import it there.` : (issue.error_code ?? issue.status).replaceAll("_", " ")
                                                            ]
                                                        }, issue.id, true, {
                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                            lineNumber: 516,
                                                            columnNumber: 25
                                                        }, this))
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 509,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                                                className: "panel library",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "library-heading",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                children: [
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                                                        children: [
                                                                            "Source library",
                                                                            " ",
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                className: "count",
                                                                                children: visibleDocs.length
                                                                            }, void 0, false, {
                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                lineNumber: 533,
                                                                                columnNumber: 27
                                                                            }, this)
                                                                        ]
                                                                    }, void 0, true, {
                                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                                        lineNumber: 531,
                                                                        columnNumber: 25
                                                                    }, this),
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                        children: "Original records, preserved exactly as uploaded."
                                                                    }, void 0, false, {
                                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                                        lineNumber: 535,
                                                                        columnNumber: 25
                                                                    }, this)
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 530,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                className: "snapshot-picker",
                                                                children: [
                                                                    "Source snapshot",
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                                                        "aria-label": "Source snapshot",
                                                                        value: snapshotId,
                                                                        onChange: (event)=>{
                                                                            setSnapshotId(event.target.value);
                                                                            setSource(null);
                                                                            sourceRequest.current += 1;
                                                                        },
                                                                        children: [
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                                                value: "",
                                                                                children: [
                                                                                    "Latest",
                                                                                    snapshots[0] ? ` · v${snapshots[0].sequence}` : ""
                                                                                ]
                                                                            }, void 0, true, {
                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                lineNumber: 548,
                                                                                columnNumber: 27
                                                                            }, this),
                                                                            snapshots.map((value)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                                                    value: value.id,
                                                                                    children: [
                                                                                        "v",
                                                                                        value.sequence,
                                                                                        " · ",
                                                                                        value.manifest.length,
                                                                                        " ",
                                                                                        "sources"
                                                                                    ]
                                                                                }, value.id, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 553,
                                                                                    columnNumber: 29
                                                                                }, this))
                                                                        ]
                                                                    }, void 0, true, {
                                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                                        lineNumber: 539,
                                                                        columnNumber: 25
                                                                    }, this)
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 537,
                                                                columnNumber: 23
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 529,
                                                        columnNumber: 21
                                                    }, this),
                                                    snapshotId && snapshotId !== snapshots[0]?.id && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "historical",
                                                        children: "Viewing an older source snapshot. Newer imports are not included."
                                                    }, void 0, false, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 562,
                                                        columnNumber: 23
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "evidence-grid",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                className: "document-list",
                                                                children: [
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                        className: "search",
                                                                        children: [
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                children: "⌕"
                                                                            }, void 0, false, {
                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                lineNumber: 570,
                                                                                columnNumber: 27
                                                                            }, this),
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                                "aria-label": "Filter sources",
                                                                                value: query,
                                                                                onChange: (event)=>setQuery(event.target.value),
                                                                                placeholder: "Find a source…"
                                                                            }, void 0, false, {
                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                lineNumber: 571,
                                                                                columnNumber: 27
                                                                            }, this)
                                                                        ]
                                                                    }, void 0, true, {
                                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                                        lineNumber: 569,
                                                                        columnNumber: 25
                                                                    }, this),
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                        className: "document-scroll",
                                                                        children: [
                                                                            visibleDocs.map((doc)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                                                    className: `document ${source?.id === doc.id ? "selected" : ""}`,
                                                                                    onClick: ()=>void openSource(doc.id),
                                                                                    children: [
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                            className: "doc-icon",
                                                                                            children: "TXT"
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 585,
                                                                                            columnNumber: 31
                                                                                        }, this),
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                            children: [
                                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                                                                    children: doc.declared_id ?? "Text record"
                                                                                                }, void 0, false, {
                                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                                    lineNumber: 587,
                                                                                                    columnNumber: 33
                                                                                                }, this),
                                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                                    className: "filename",
                                                                                                    children: doc.filename
                                                                                                }, void 0, false, {
                                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                                    lineNumber: 590,
                                                                                                    columnNumber: 33
                                                                                                }, this),
                                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                                                                                    children: [
                                                                                                        doc.line_count,
                                                                                                        " lines ",
                                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                                            children: "·"
                                                                                                        }, void 0, false, {
                                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                                            lineNumber: 592,
                                                                                                            columnNumber: 58
                                                                                                        }, this),
                                                                                                        " ",
                                                                                                        (doc.byte_count / 1024).toFixed(1),
                                                                                                        " KiB"
                                                                                                    ]
                                                                                                }, void 0, true, {
                                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                                    lineNumber: 591,
                                                                                                    columnNumber: 33
                                                                                                }, this)
                                                                                            ]
                                                                                        }, void 0, true, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 586,
                                                                                            columnNumber: 31
                                                                                        }, this),
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                            className: "chevron",
                                                                                            children: "›"
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 596,
                                                                                            columnNumber: 31
                                                                                        }, this)
                                                                                    ]
                                                                                }, doc.id, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 580,
                                                                                    columnNumber: 29
                                                                                }, this)),
                                                                            !visibleDocs.length && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                                className: "empty small",
                                                                                children: query ? "No sources match your search." : "Your source records will appear here after import."
                                                                            }, void 0, false, {
                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                lineNumber: 600,
                                                                                columnNumber: 29
                                                                            }, this)
                                                                        ]
                                                                    }, void 0, true, {
                                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                                        lineNumber: 578,
                                                                        columnNumber: 25
                                                                    }, this),
                                                                    viewingLatest && withdrawnDocs.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                                                        className: "withdrawn",
                                                                        children: [
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                                                children: [
                                                                                    "Removed from case (",
                                                                                    withdrawnDocs.length,
                                                                                    ")"
                                                                                ]
                                                                            }, void 0, true, {
                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                lineNumber: 609,
                                                                                columnNumber: 29
                                                                            }, this),
                                                                            withdrawnDocs.map((doc)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                                    className: "withdrawn-row",
                                                                                    children: [
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                                                            className: "text-action",
                                                                                            onClick: ()=>void openSource(doc.id),
                                                                                            children: doc.declared_id ?? doc.filename
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 614,
                                                                                            columnNumber: 33
                                                                                        }, this),
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                                                            className: "text-action",
                                                                                            disabled: busy,
                                                                                            onClick: ()=>void changeDocument(doc.id, "restore"),
                                                                                            children: "Restore"
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 620,
                                                                                            columnNumber: 33
                                                                                        }, this)
                                                                                    ]
                                                                                }, doc.id, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 613,
                                                                                    columnNumber: 31
                                                                                }, this))
                                                                        ]
                                                                    }, void 0, true, {
                                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                                        lineNumber: 608,
                                                                        columnNumber: 27
                                                                    }, this)
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 568,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                className: "source-viewer",
                                                                "aria-busy": loadingSource,
                                                                children: loadingSource ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                    className: "empty",
                                                                    role: "status",
                                                                    children: "Opening source…"
                                                                }, void 0, false, {
                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                    lineNumber: 636,
                                                                    columnNumber: 27
                                                                }, this) : source ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                                                    children: [
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            className: "source-heading",
                                                                            children: [
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                                    children: [
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                            className: "eyebrow",
                                                                                            children: "ORIGINAL SOURCE"
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 643,
                                                                                            columnNumber: 33
                                                                                        }, this),
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                                                                            children: source.declared_id ?? source.filename
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 644,
                                                                                            columnNumber: 33
                                                                                        }, this),
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                                            children: source.filename
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 645,
                                                                                            columnNumber: 33
                                                                                        }, this)
                                                                                    ]
                                                                                }, void 0, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 642,
                                                                                    columnNumber: 31
                                                                                }, this),
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                    className: "verified",
                                                                                    children: sourceWithdrawn ? "● Removed from case" : "● Preserved"
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 647,
                                                                                    columnNumber: 31
                                                                                }, this)
                                                                            ]
                                                                        }, void 0, true, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 641,
                                                                            columnNumber: 29
                                                                        }, this),
                                                                        viewingLatest && !sourceWithdrawn && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            className: "remove-source",
                                                                            children: [
                                                                                removing ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                                                                                    onSubmit: (event)=>{
                                                                                        event.preventDefault();
                                                                                        void changeDocument(source.id, "withdraw", removeReason.trim());
                                                                                    },
                                                                                    children: [
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                                            "aria-label": "Reason for removal",
                                                                                            placeholder: "Reason (for example, filed to the wrong chart)",
                                                                                            value: removeReason,
                                                                                            maxLength: 500,
                                                                                            onChange: (event)=>setRemoveReason(event.target.value)
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 666,
                                                                                            columnNumber: 37
                                                                                        }, this),
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                                                            disabled: busy || !removeReason.trim(),
                                                                                            children: "Remove"
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 675,
                                                                                            columnNumber: 37
                                                                                        }, this),
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                                                            type: "button",
                                                                                            className: "text-action",
                                                                                            onClick: ()=>setRemoving(false),
                                                                                            children: "Cancel"
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 680,
                                                                                            columnNumber: 37
                                                                                        }, this)
                                                                                    ]
                                                                                }, void 0, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 656,
                                                                                    columnNumber: 35
                                                                                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                                                    className: "text-action",
                                                                                    onClick: ()=>setRemoving(true),
                                                                                    children: "Remove from case…"
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 689,
                                                                                    columnNumber: 35
                                                                                }, this),
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("small", {
                                                                                    children: "The original stays preserved for audit. A new source snapshot without it is analysed automatically; it can be restored later."
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 696,
                                                                                    columnNumber: 33
                                                                                }, this)
                                                                            ]
                                                                        }, void 0, true, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 654,
                                                                            columnNumber: 31
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            className: "source-meta",
                                                                            children: [
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                    children: [
                                                                                        "SHA-256",
                                                                                        " ",
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                                                                                            title: source.sha256,
                                                                                            children: [
                                                                                                source.sha256.slice(0, 16),
                                                                                                "…"
                                                                                            ]
                                                                                        }, void 0, true, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 706,
                                                                                            columnNumber: 33
                                                                                        }, this)
                                                                                    ]
                                                                                }, void 0, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 704,
                                                                                    columnNumber: 31
                                                                                }, this),
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                    children: [
                                                                                        source.line_count,
                                                                                        " lines"
                                                                                    ]
                                                                                }, void 0, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 710,
                                                                                    columnNumber: 31
                                                                                }, this)
                                                                            ]
                                                                        }, void 0, true, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 703,
                                                                            columnNumber: 29
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                            className: "span-picker",
                                                                            children: [
                                                                                "Inspect a source block",
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                                                                    "aria-label": "Source block",
                                                                                    value: spanId,
                                                                                    onChange: (event)=>setSpanId(event.target.value),
                                                                                    children: [
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                                                            value: "",
                                                                                            children: "All source lines"
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 721,
                                                                                            columnNumber: 33
                                                                                        }, this),
                                                                                        source.spans.map((span)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                                                                value: span.id,
                                                                                                children: [
                                                                                                    "Lines ",
                                                                                                    span.start_line,
                                                                                                    "–",
                                                                                                    span.end_line,
                                                                                                    ":",
                                                                                                    " ",
                                                                                                    span.quote.slice(0, 70)
                                                                                                ]
                                                                                            }, span.id, true, {
                                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                                lineNumber: 723,
                                                                                                columnNumber: 35
                                                                                            }, this))
                                                                                    ]
                                                                                }, void 0, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 714,
                                                                                    columnNumber: 31
                                                                                }, this)
                                                                            ]
                                                                        }, void 0, true, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 712,
                                                                            columnNumber: 29
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            className: "source-lines",
                                                                            tabIndex: 0,
                                                                            "aria-label": "Original source text",
                                                                            children: lines.map((line, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                                    id: `line-${i + 1}`,
                                                                                    className: `source-line ${highlighted && i + 1 >= highlighted.start_line && i + 1 <= highlighted.end_line ? "highlighted" : ""}`,
                                                                                    children: [
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                            className: "line-number",
                                                                                            "aria-hidden": "true",
                                                                                            children: i + 1
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 741,
                                                                                            columnNumber: 35
                                                                                        }, this),
                                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                            children: line || " "
                                                                                        }, void 0, false, {
                                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                                            lineNumber: 747,
                                                                                            columnNumber: 35
                                                                                        }, this)
                                                                                    ]
                                                                                }, i, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 736,
                                                                                    columnNumber: 33
                                                                                }, this))
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 730,
                                                                            columnNumber: 29
                                                                        }, this),
                                                                        highlighted && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            className: "citation-detail",
                                                                            children: [
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                                                    children: [
                                                                                        "Stable citation · lines",
                                                                                        " ",
                                                                                        highlighted.start_line,
                                                                                        "–",
                                                                                        highlighted.end_line
                                                                                    ]
                                                                                }, void 0, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 753,
                                                                                    columnNumber: 33
                                                                                }, this),
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                    children: [
                                                                                        "Character offsets [",
                                                                                        highlighted.start_char,
                                                                                        ",",
                                                                                        " ",
                                                                                        highlighted.end_char,
                                                                                        ")"
                                                                                    ]
                                                                                }, void 0, true, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 758,
                                                                                    columnNumber: 33
                                                                                }, this),
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                                                                                    href: `/api/v1/source-revisions/${source.id}/spans/${highlighted.id}`,
                                                                                    target: "_blank",
                                                                                    rel: "noreferrer",
                                                                                    children: "Open citation data ↗"
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 762,
                                                                                    columnNumber: 33
                                                                                }, this)
                                                                            ]
                                                                        }, void 0, true, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 752,
                                                                            columnNumber: 31
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            className: "source-footer",
                                                                            children: "Blocks are structural text sections. Use the Abstraction view to inspect extracted clinical meaning and document status."
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 771,
                                                                            columnNumber: 29
                                                                        }, this)
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                    lineNumber: 640,
                                                                    columnNumber: 27
                                                                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                    className: "empty source-empty",
                                                                    children: [
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            className: "empty-icon",
                                                                            children: "▤"
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 779,
                                                                            columnNumber: 29
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                                                            children: "Follow the evidence"
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 780,
                                                                            columnNumber: 29
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                            children: [
                                                                                "Select a record to inspect its original text,",
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("br", {}, void 0, false, {
                                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                                    lineNumber: 783,
                                                                                    columnNumber: 31
                                                                                }, this),
                                                                                "line numbers, and exact source spans."
                                                                            ]
                                                                        }, void 0, true, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 781,
                                                                            columnNumber: 29
                                                                        }, this)
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                    lineNumber: 778,
                                                                    columnNumber: 27
                                                                }, this)
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 634,
                                                                columnNumber: 23
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 567,
                                                        columnNumber: 21
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 528,
                                                columnNumber: 19
                                            }, this),
                                            jobs.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                                className: "panel import-history",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                                        children: [
                                                            "Import history",
                                                            " ",
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "count",
                                                                children: jobs.length
                                                            }, void 0, false, {
                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                lineNumber: 795,
                                                                columnNumber: 25
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                        lineNumber: 793,
                                                        columnNumber: 23
                                                    }, this),
                                                    [
                                                        ...jobs
                                                    ].sort((a, b)=>b.created_at.localeCompare(a.created_at)).map((job)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            className: "job",
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                    children: [
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                                            children: new Date(job.created_at).toLocaleString()
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 804,
                                                                            columnNumber: 31
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                            className: "job-status",
                                                                            children: job.status === "succeeded" ? "Processing complete" : job.status
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 807,
                                                                            columnNumber: 31
                                                                        }, this),
                                                                        job.error_code && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                            children: job.error_code.replaceAll("_", " ")
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                                            lineNumber: 813,
                                                                            columnNumber: 33
                                                                        }, this)
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/apps/web/app/page.tsx",
                                                                    lineNumber: 803,
                                                                    columnNumber: 29
                                                                }, this),
                                                                job.uploads.map((file)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                        className: "upload-row",
                                                                        children: [
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                children: file.filename
                                                                            }, void 0, false, {
                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                lineNumber: 820,
                                                                                columnNumber: 33
                                                                            }, this),
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                className: `upload-status ${file.status}`,
                                                                                children: file.status
                                                                            }, void 0, false, {
                                                                                fileName: "[project]/apps/web/app/page.tsx",
                                                                                lineNumber: 821,
                                                                                columnNumber: 33
                                                                            }, this)
                                                                        ]
                                                                    }, file.id, true, {
                                                                        fileName: "[project]/apps/web/app/page.tsx",
                                                                        lineNumber: 819,
                                                                        columnNumber: 31
                                                                    }, this))
                                                            ]
                                                        }, job.id, true, {
                                                            fileName: "[project]/apps/web/app/page.tsx",
                                                            lineNumber: 802,
                                                            columnNumber: 27
                                                        }, this))
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 792,
                                                columnNumber: 21
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 472,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("footer", {
                                        children: [
                                            "Source-grounded by design ",
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                children: "·"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 835,
                                                columnNumber: 43
                                            }, this),
                                            " Claude drafts require review",
                                            " ",
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                onClick: async ()=>{
                                                    if (!session) return;
                                                    try {
                                                        await (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])("/session", {
                                                            method: "DELETE",
                                                            headers: {
                                                                "X-CSRF-Token": session.csrf_token
                                                            }
                                                        });
                                                        setSession(null);
                                                        setPatient(null);
                                                        setPatients([]);
                                                    } catch (error) {
                                                        setError(message(error));
                                                    }
                                                },
                                                children: "Sign out"
                                            }, void 0, false, {
                                                fileName: "[project]/apps/web/app/page.tsx",
                                                lineNumber: 837,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/apps/web/app/page.tsx",
                                        lineNumber: 834,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/page.tsx",
                                lineNumber: 361,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/page.tsx",
                        lineNumber: 322,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/page.tsx",
                lineNumber: 306,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/page.tsx",
        lineNumber: 264,
        columnNumber: 5
    }, this);
}
_s(Workspace, "Vm5p0JIwPtM/1aSU9Syc0YSA1mI=");
_c = Workspace;
var _c;
__turbopack_context__.k.register(_c, "Workspace");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/app/readable-abstraction-view.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ReadableAbstractionView",
    ()=>ReadableAbstractionView
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/lib/api.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/apps/web/app/evidence-views.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
function ReadableAbstractionView({ run, onSource }) {
    _s();
    const state = run.result?.readable_abstraction;
    const [selected, setSelected] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [query, setQuery] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [showSource, setShowSource] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(true);
    const [source, setSource] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [sourceError, setSourceError] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const current = state?.documents.find((d)=>d.profile.revision_id === selected) ?? state?.documents[0];
    const revision = current?.profile.revision_id;
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ReadableAbstractionView.useEffect": ()=>{
            let cancelled = false;
            setSource(null);
            setSourceError("");
            if (revision && showSource) {
                (0, __TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["api"])(`/source-revisions/${revision}`).then({
                    "ReadableAbstractionView.useEffect": (value)=>{
                        if (!cancelled) setSource(value);
                    }
                }["ReadableAbstractionView.useEffect"]).catch({
                    "ReadableAbstractionView.useEffect": ()=>{
                        if (!cancelled) setSourceError("Unable to load the original document.");
                    }
                }["ReadableAbstractionView.useEffect"]);
            }
            return ({
                "ReadableAbstractionView.useEffect": ()=>{
                    cancelled = true;
                }
            })["ReadableAbstractionView.useEffect"];
        }
    }["ReadableAbstractionView.useEffect"], [
        revision,
        showSource
    ]);
    if (!state || !current) return null;
    const citations = run.result?.citations ?? [];
    const cite = (ids)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$apps$2f$web$2f$app$2f$evidence$2d$views$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["References"], {
            ids: ids,
            citations: citations,
            onSource: onSource
        }, void 0, false, {
            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
            lineNumber: 49,
            columnNumber: 5
        }, this);
    const profile = current.profile;
    const review = state.reviews?.find((r)=>r.target_ref === revision);
    const comparisonReview = state.reviews?.find((r)=>r.target_ref === "synthesis");
    const matching = (text)=>text.toLowerCase().includes(query.toLowerCase());
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "readable-abstraction",
        children: [
            state.limitations.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "alert warning",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                        children: "Incomplete abstraction"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 62,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        children: "Some documents or comparisons need attention. Answers must preserve these gaps."
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 63,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                children: [
                                    "Show details (",
                                    state.limitations.length,
                                    ")"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 68,
                                columnNumber: 13
                            }, this),
                            state.limitations.map((text, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    children: text
                                }, i, false, {
                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                    lineNumber: 70,
                                    columnNumber: 15
                                }, this))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 67,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                lineNumber: 61,
                columnNumber: 9
            }, this),
            state.synthesis && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                className: "readable-overview",
                open: true,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                        children: "Across the documents"
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 77,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "muted-text",
                        children: comparisonReview?.status === "checked" ? "Compared with source evidence. Conflicts and source accounts remain preserved." : "Draft comparison — evidence review is incomplete or found issues."
                    }, void 0, false, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 78,
                        columnNumber: 11
                    }, this),
                    state.synthesis.overview.map((fact, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    children: fact.text
                                }, void 0, false, {
                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                    lineNumber: 85,
                                    columnNumber: 15
                                }, this),
                                cite(fact.citations)
                            ]
                        }, i, true, {
                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                            lineNumber: 84,
                            columnNumber: 13
                        }, this)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                children: [
                                    "Related records and differences (",
                                    state.synthesis.connections.length,
                                    ")"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 90,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "muted-text",
                                children: "Evidence-based comparisons. Each source account remains preserved."
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 94,
                                columnNumber: 13
                            }, this),
                            state.synthesis.connections.map((connection, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                            children: connection.kind.replaceAll("_", " ")
                                        }, void 0, false, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 99,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            className: "muted-text",
                                            children: [
                                                " ",
                                                "·",
                                                " ",
                                                state.decisions?.find((d)=>d.proposal_path === `/connections/${i}`)?.status.replaceAll("_", " ") ?? "proposal"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 100,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            children: connection.text
                                        }, void 0, false, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 107,
                                            columnNumber: 17
                                        }, this),
                                        cite(connection.citations)
                                    ]
                                }, i, true, {
                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                    lineNumber: 98,
                                    columnNumber: 15
                                }, this))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 89,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                lineNumber: 76,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "readable-controls",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            "Document (",
                            state.documents.length,
                            ")",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                value: profile.revision_id,
                                onChange: (event)=>{
                                    setSelected(event.target.value);
                                    setQuery("");
                                },
                                children: state.documents.map((doc)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: doc.profile.revision_id,
                                        children: [
                                            doc.profile.title,
                                            " ·",
                                            " ",
                                            run.result?.document_sources?.find((s)=>s.revision_id === doc.profile.revision_id)?.filename
                                        ]
                                    }, doc.profile.revision_id, true, {
                                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                        lineNumber: 125,
                                        columnNumber: 15
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 117,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 115,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        children: [
                            "Find in this abstraction",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                placeholder: "Search clinical details",
                                value: query,
                                onChange: (e)=>setQuery(e.target.value)
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 141,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 139,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        className: "readable-toggle",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                type: "checkbox",
                                checked: showSource,
                                onChange: (e)=>setShowSource(e.target.checked)
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 148,
                                columnNumber: 11
                            }, this),
                            " ",
                            "Original beside abstraction"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 147,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                lineNumber: 114,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: `readable-comparison ${showSource ? "with-source" : ""}`,
                children: [
                    showSource && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                        className: "readable-original",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                children: "Original document"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 159,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                                children: sourceError || source?.text || "Loading original…"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 160,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 158,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                        className: "readable-document",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                children: profile.title
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 164,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "muted-text",
                                children: review?.status === "checked" ? "Source check completed — no issues flagged." : review ? "Needs source review" : "Source verification not run for this version"
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 165,
                                columnNumber: 11
                            }, this),
                            review?.report?.issues.map((issue, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                    className: "alert warning",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            children: issue.detail
                                        }, void 0, false, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 174,
                                            columnNumber: 15
                                        }, this),
                                        cite(issue.citations)
                                    ]
                                }, i, true, {
                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                    lineNumber: 173,
                                    columnNumber: 13
                                }, this)),
                            review?.error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "alert warning",
                                children: "The source check could not finish. Retry this abstraction to check it."
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 179,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "muted-text",
                                children: [
                                    profile.document_type.replaceAll("_", " "),
                                    profile.stated_status ? ` · ${profile.stated_status}` : ""
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 184,
                                columnNumber: 11
                            }, this),
                            profile.contributors.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                children: profile.contributors.map((c)=>`${c.name} (${c.scope})`).join("; ")
                            }, void 0, false, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 189,
                                columnNumber: 13
                            }, this),
                            profile.signatures.map((s, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                            children: [
                                                s.kind,
                                                ":"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 197,
                                            columnNumber: 15
                                        }, this),
                                        " ",
                                        s.name,
                                        " ·",
                                        " ",
                                        s.when ? `${s.when.date}${s.when.time ? ` ${s.when.time}` : ""}` : "Date not stated",
                                        " ",
                                        "· ",
                                        s.scope
                                    ]
                                }, i, true, {
                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                    lineNumber: 196,
                                    columnNumber: 13
                                }, this)),
                            current.sections.map((section, i)=>{
                                const facts = section.facts.filter((f)=>matching(`${section.heading} ${f.text}`));
                                return facts.length ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h4", {
                                            children: section.heading
                                        }, void 0, false, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 210,
                                            columnNumber: 17
                                        }, this),
                                        facts.map((fact, j)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                        children: fact.text
                                                    }, void 0, false, {
                                                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                        lineNumber: 213,
                                                        columnNumber: 21
                                                    }, this),
                                                    cite(fact.citations)
                                                ]
                                            }, j, true, {
                                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                lineNumber: 212,
                                                columnNumber: 19
                                            }, this))
                                    ]
                                }, i, true, {
                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                    lineNumber: 209,
                                    columnNumber: 15
                                }, this) : null;
                            }),
                            current.contacts.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                        children: "Contact times and participation"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                        lineNumber: 222,
                                        columnNumber: 15
                                    }, this),
                                    current.contacts.map((contact, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h4", {
                                                    children: [
                                                        contact.service_date ?? "Date unstated",
                                                        " ·",
                                                        " ",
                                                        contact.service
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                    lineNumber: 225,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    children: [
                                                        contact.encounter_id,
                                                        " · ",
                                                        contact.attendance
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                    lineNumber: 229,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    children: contact.participants
                                                }, void 0, false, {
                                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                    lineNumber: 232,
                                                    columnNumber: 19
                                                }, this),
                                                contact.intervals.map((interval, j)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                children: [
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                                        children: [
                                                                            interval.purpose.replaceAll("_", " "),
                                                                            ":"
                                                                        ]
                                                                    }, void 0, true, {
                                                                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                                        lineNumber: 236,
                                                                        columnNumber: 25
                                                                    }, this),
                                                                    " ",
                                                                    interval.start ?? "Start unknown",
                                                                    " –",
                                                                    " ",
                                                                    interval.end ?? "End unknown",
                                                                    interval.documented_minutes !== null ? ` · ${interval.documented_minutes} documented minutes` : "",
                                                                    ". ",
                                                                    interval.participants,
                                                                    ". ",
                                                                    interval.qualification
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                                lineNumber: 235,
                                                                columnNumber: 23
                                                            }, this),
                                                            cite(interval.citations)
                                                        ]
                                                    }, j, true, {
                                                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                        lineNumber: 234,
                                                        columnNumber: 21
                                                    }, this))
                                            ]
                                        }, i, true, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 224,
                                            columnNumber: 17
                                        }, this))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 221,
                                columnNumber: 13
                            }, this),
                            current.assessments.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                        children: "Assessment values"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                        lineNumber: 255,
                                        columnNumber: 15
                                    }, this),
                                    current.assessments.map((a, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                            children: [
                                                                a.instrument,
                                                                a.item ? ` · ${a.item}` : "",
                                                                ":"
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                            lineNumber: 259,
                                                            columnNumber: 21
                                                        }, this),
                                                        " ",
                                                        a.score ?? "Score unstated",
                                                        " ·",
                                                        " ",
                                                        a.completed_on ?? "Completion date unstated"
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                    lineNumber: 258,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    children: a.context
                                                }, void 0, false, {
                                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                    lineNumber: 266,
                                                    columnNumber: 19
                                                }, this),
                                                cite(a.citations)
                                            ]
                                        }, i, true, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 257,
                                            columnNumber: 17
                                        }, this))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 254,
                                columnNumber: 13
                            }, this),
                            profile.dates.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                                        children: "Document and event dates"
                                    }, void 0, false, {
                                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                        lineNumber: 274,
                                        columnNumber: 15
                                    }, this),
                                    profile.dates.map((d, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    children: [
                                                        d.when.date,
                                                        " ",
                                                        d.when.time,
                                                        " · ",
                                                        d.kind,
                                                        " · ",
                                                        d.scope
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                                    lineNumber: 277,
                                                    columnNumber: 19
                                                }, this),
                                                cite(d.citations)
                                            ]
                                        }, i, true, {
                                            fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                            lineNumber: 276,
                                            columnNumber: 17
                                        }, this))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                                lineNumber: 273,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                        lineNumber: 163,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
                lineNumber: 156,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/apps/web/app/readable-abstraction-view.tsx",
        lineNumber: 59,
        columnNumber: 5
    }, this);
}
_s(ReadableAbstractionView, "jtBuupGNMcFDxcFzmRYBNRMnjEU=");
_c = ReadableAbstractionView;
var _c;
__turbopack_context__.k.register(_c, "ReadableAbstractionView");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/apps/web/lib/api.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "allPages",
    ()=>allPages,
    "api",
    ()=>api
]);
async function api(path, init = {}) {
    const response = await fetch(`/api/v1${path}`, {
        ...init,
        cache: "no-store"
    });
    if (!response.ok) {
        const error = await response.json().catch(()=>({
                detail: "request_failed"
            }));
        const code = typeof error.detail === "string" ? error.detail : "request_failed";
        throw new Error(`${response.status}: ${code.replaceAll("_", " ")}`);
    }
    if (response.status === 204) return undefined;
    return response.json();
}
async function allPages(path) {
    const rows = [];
    let cursor = "";
    for(;;){
        const page = await api(`${path}${cursor ? `?after=${cursor}` : ""}`);
        rows.push(...page);
        if (page.length < 100) return rows;
        cursor = page[page.length - 1].id;
    }
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=apps_web_20sk34m._.js.map