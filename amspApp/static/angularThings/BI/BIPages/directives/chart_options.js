function chart_option_1(
    element,
    scope
    // chart_instance
) {
    function chart_option_hover_1(event, chartElement) {
        event.native.target.style.cursor = chartElement[0] ? 'pointer' : 'default';
    }

    function chart_option_animation_1() {
        let delayed;
        return {
            onComplete: () => {
                delayed = true;
            },
            delay: (context) => {
                let delay = 0;
                if (context.type === 'data' && context.mode === 'default' && !delayed) {
                    delay = context.dataIndex * 300 + context.datasetIndex * 100;
                }
                return delay;
            },
        }
    }

    function chart_option_plugin_1() {
        return {
            datalabels: {
                color: '#696969',
                align: 'top',
                anchor: 'end',
                labels: {
                    title: {
                        font: {
                            family: "'Yekan'"
                        }
                    }
                }
            },
            title: {
                display: true,

                // text: scope.currentcell.title,
                text: scope.chart_data.title,
                font: {
                    family: "'Yekan'",
                    size: 14
                }
            },
            elements: {
                bar: {
                    borderRadius: 3,
                }

            },
            tooltip: {
                bodyFont: {
                    family: "'Yekan'",
                    size: 14
                },
                footerFont: {
                    family: "'Yekan'",
                    size: 14
                },
                titleFont: {
                    family: "'Yekan'",
                    size: 14
                },
                rtl: true,
            },
            subtitle: {
                display: true,
                text: (scope.chart_data.description) ? scope.chart_data.description : '-',
                // text: 'آخرین اطلاعات وارد شده : ' + 'scope.step[scope['''current_step''']].data.last_insert.toFaDigit()',
                font: {
                    family: "'Yekan'",
                }
            },
            legend: {
                display: true,
                labels: {
                    font: {
                        family: "'Yekan'"
                    }
                }
            }
        }
    }

    function chart_option_scales_1() {
        return {
            y: {

                beginAtZero: true,
                ticks: {
                    font: {
                        family: "'Yekan'"
                    }
                }

            },
            x: {
                beginAtZero: true,
                ticks: {
                    font: {
                        family: "'Yekan'"
                    }
                }

            }
        }
    }


    return {
        aspectRatio: 2,
        onHover: chart_option_hover_1,
        onClick: (event, chartElement) => {
            if (chartElement[0]) {
                if (chartElement[0].datasetIndex === 0) {
                    // scope.request.level = scope.request.level + 1;
                    scope.request.level = scope.chart_data.level + 1;
                    scope.request.dataset_index = chartElement[0].datasetIndex;
                    scope.request.selected_value_index = chartElement[0].index;
                    scope.get_request_data();
                }
            }
            // if (scope.loading){
            //     return
            // }
            // if (chartElement[0]) {
            //     if (chartElement[0].datasetIndex === 0) {
            //         let req = {}
            //         req['chart_id'] = scope.step[scope.current_step].request.chart_id;
            //         req['groupby_index'] = scope.current_step + 1;
            //         req['groupby_value'] = chartElement[0].index;
            //         req['groupby_dataset_index'] = chartElement[0].datasetIndex;
            //         req['chart_type'] = scope.step[scope.current_step].request.chart_type;
            //         scope.get_data(req);
            //     }
            // }
        },
        animation: chart_option_animation_1(),
        locale: 'fa-IR',
        responsive: false,
        maintainAspectRatio: false,
        plugins: chart_option_plugin_1(),
        scales: chart_option_scales_1(),
    }
}

