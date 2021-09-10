import json
import os
import PySimpleGUI as sg

import calculate_rating


impact_options = ["High", "Considerable", "Moderate", "Limited", "Low"]
likelihood_options = ["Almost Certain", "Likely", "Possible", "Unlikely", "Remote"]
status_options = ["Open", "Closed", "Closed Pending Confirmation"]

mline_width = 67


def expando(key):
    # return sg.Submit("↗", key=key, tooltip="Expand")
    return sg.Text("↗", key=key, tooltip="Expand", enable_events=True, metadata="↗")


def hideo(key):
    return sg.Text(
        "(hide)",
        key=key,
        font="Consolas 8 underline",
        enable_events=True,
        metadata="hide",
    )


def section(title, content):
    return [
        [
            sg.Text(title.title(), size=(15, 1)),
            sg.Column(
                [
                    [
                        hideo("hide_" + title),
                        expando("expand_" + title),
                    ]
                ],
                element_justification="right",
                vertical_alignment="bottom",
                expand_x=True,
            ),
        ],
        sg.pin(
            sg.Column(
                [
                    [sg.Multiline(content, key=title, size=(mline_width, 5))],
                ],
                key="col_" + title,
            )
        ),
    ]


def section_combo(title, content, options, default_value):
    return (
        [
            [
                sg.Text(title.title(), size=(15, 1)),
                sg.Column(
                    [
                        [
                            hideo("hide_" + title),
                            sg.Combo(
                                options,
                                default_value=default_value,
                                key="rating_" + title,
                                readonly=True,
                                enable_events=True,
                            ),
                            expando("expand_" + title),
                        ]
                    ],
                    element_justification="right",
                    vertical_alignment="bottom",
                    expand_x=True,
                ),
            ],
            sg.pin(
                sg.Column(
                    [
                        [sg.Multiline(content, key=title, size=(mline_width, 5))],
                    ],
                    key="col_" + title,
                )
            ),
        ],
    )


def layout(vuln, scan_id):
    input_width = 45
    num_items_to_show = 4

    print(vuln)

    # Description
    description = vuln["description"] if vuln and "description" in vuln else ""

    # Replication
    replication = vuln["replication"] if vuln and "replication" in vuln else ""

    # Impact
    impact = vuln["impact"] if vuln and "impact" in vuln else ""

    # Likelihood
    likelihood = vuln["likelihood"] if vuln and "likelihood" in vuln else ""

    # Remediation
    remediation = vuln["remediation"] if vuln and "remediation" in vuln else ""

    # CWE
    cwe = vuln["cwe"] if vuln and "cwe" in vuln else ""

    # Title
    title = vuln["title"] if vuln and "title" in vuln else ""

    # Status
    status = vuln["status"] if vuln and "status" in vuln else ""
    if status not in status_options:
        status = "Open"

    # Impact
    impact_rating = vuln["rating_impact"] if vuln and "rating_impact" in vuln else ""
    if impact_rating not in impact_options:
        impact_rating = ""

    # Likelihood
    likelihood_rating = (
        vuln["rating_likelihood"] if vuln and "rating_likelihood" in vuln else ""
    )
    if likelihood_rating not in likelihood_options:
        likelihood_rating = ""

    # Severity
    severity, text_color = None, None
    try:
        severity = calculate_rating.calculate_rating(impact_rating, likelihood_rating)
        severity, text_color = calculate_rating.calculate_rating(
            impact_rating, likelihood_rating
        )
    except:
        pass

    return [
        [
            sg.Column(
                [
                    [sg.Input(key="vuln_name", default_text=scan_id, visible=False)],
                    [
                        sg.Text("Scan Id", size=(15, 1)),
                        sg.Input(key="scanid", default_text=scan_id),
                    ],
                    [
                        sg.Text("Title", size=(15, 1)),
                        sg.Input(title, key="title", enable_events=True),
                    ],
                    [
                        sg.pin(
                            sg.Column(
                                [
                                    [
                                        sg.Listbox(
                                            values=[],
                                            size=(input_width, num_items_to_show),
                                            enable_events=True,
                                            key="-BOX-TITLE",
                                            select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                                            no_scrollbar=True,
                                            pad=((139, 0), (2, 2)),
                                        )
                                    ]
                                ],
                                key="-BOX-TITLE-CONTAINER-",
                                pad=(0, 0),
                                visible=False,
                            )
                        )
                    ],
                    [
                        sg.Text("CWE", size=(15, 1)),
                        sg.Input(cwe, key="cwe", enable_events=True),
                    ],
                    [
                        sg.pin(
                            sg.Column(
                                [
                                    [
                                        sg.Listbox(
                                            values=[],
                                            size=(input_width, num_items_to_show),
                                            enable_events=True,
                                            key="-BOX-CWE",
                                            select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                                            no_scrollbar=True,
                                            pad=((139, 0), (2, 2)),
                                        )
                                    ]
                                ],
                                key="-BOX-CWE-CONTAINER-",
                                pad=(0, 0),
                                visible=False,
                            )
                        )
                    ],
                    [
                        sg.Text("Status", size=(15, 1)),
                        sg.Combo(
                            status_options,
                            default_value=status,
                            key="status",
                            readonly=True,
                            enable_events=True,
                        ),
                    ],
                    [
                        sg.Text("Severity", size=(15, 1)),
                        sg.Text(
                            severity,
                            key="severity_rating",
                            size=(40, 1),
                            text_color=text_color,
                        ),
                    ],
                ],
                element_justification="left",
            ),
            sg.Column(
                [
                    [
                        sg.Text(
                            "💾",
                            key="save_vuln",
                            enable_events=True,
                            tooltip="Save",
                            font="Consolas 20",
                        )
                    ],
                    [
                        sg.Text(
                            "↗",
                            key="export",
                            size=(1, 1),
                            tooltip="Export as Template",
                            enable_events=True,
                        ),
                        sg.Text(
                            "?",
                            key="info",
                            size=(1, 1),
                            tooltip="Links for vulnerability information",
                            enable_events=True,
                        ),
                    ],
                ],
                element_justification="right",
                vertical_alignment="top",
            ),
        ],
        section("description", description),
        [sg.HorizontalSeparator(pad=(5, 10))],
        section("replication", replication),
        [sg.HorizontalSeparator(pad=(5, 10))],
        section_combo("impact", impact, impact_options, impact_rating),
        [sg.HorizontalSeparator(pad=(5, 10))],
        section_combo("likelihood", likelihood, likelihood_options, likelihood_rating),
        [sg.HorizontalSeparator(pad=(5, 10))],
        section("remediation", remediation),
    ]


def update_window_vuln(ctx, window, value):
    window["-BOX-CWE-CONTAINER-"].update(visible=False)
    window["-BOX-TITLE-CONTAINER-"].update(visible=False)

    cwe, title = value.split(" - ")

    template_path = os.path.join(ctx.templates_folder, value + ".json")
    if not os.path.exists(template_path):
        print("Unable to locate template file")
        return

    template_file = open(template_path, "r")

    data = None
    try:
        data = json.load(template_file)
    except:
        pass

    title = data["title"] if data and "title" in data else ""
    cwe = data["cwe"] if data and "cwe" in data else ""

    description = data["description"] if data and "description" in data else ""
    impact = data["impact"] if data and "impact" in data else ""
    likelihood = data["likelihood"] if data and "likelihood" in data else ""
    remediation = data["remediation"] if data and "remediation" in data else ""
    # metadata = data["links"] if data and "links" in data else []

    window["cwe"].Update(cwe)
    window["title"].Update(title)
    window["description"].update(value=description)
    window["impact"].update(value=impact)
    window["likelihood"].update(value=likelihood)
    window["remediation"].update(value=remediation)
    window["info"].metadata = data


def window(ctx, event, values):
    scan_id = None

    if event == "edit_vuln":
        if len(values["vuln_list"]) < 1:
            sg.popup_ok(
                "Please select a vulnerability from the list",
                title="Edit Vulnerability",
                keep_on_top=True,
            )
            return

        scan_id = values["vuln_list"][0].split(" - ")[0]

    if event == "new_vuln":
        scan_id = "Scan-XXXX" + str(ctx.vuln_count())

    vuln = ctx.get_vuln(scan_id)

    layout_vuln = layout(vuln, scan_id)
    return sg.Window(
        "PenTest - Vulnerability",
        layout_vuln,
        icon=ctx.icon(),
        finalize=True,
    )