Vue.use(Vuetify);

Vue.component('jupyter-widget-mount-point', {
    data() {
        return {
            renderFn: undefined,
            elem: undefined,
        }
    },
    props: ['mount-id'],
    created() {
        requestWidget(this.mountId);
    },
    mounted() {
        requestWidget(this.mountId)
            .then(widgetView => {
                if (['VuetifyView', 'VuetifyTemplateView'].includes(widgetView.model.get('_view_name'))) {
                    this.renderFn = createElement => widgetView.vueRender(createElement);
                } else {
                    while (this.$el.firstChild) {
                        this.$el.removeChild(this.$el.firstChild);
                    }

                    requirejs(['@jupyter-widgets/base'], widgets =>
                        widgets.JupyterPhosphorWidget.attach(widgetView.pWidget, this.$el)
                    );
                }
            }
            );
    },
    render(createElement) {
        if (this.renderFn) {
            /* workaround for v-menu click */
            if (!this.elem) {
                this.elem = this.renderFn(createElement);
            }
            return this.elem;
        }
        return createElement('div', this.$slots.default ||
            [createElement('v-chip', `[${this.mountId}]`)]);
    }
});

const widgetResolveFns = {};
const widgetPromises = {};

function provideWidget(mountId, widgetView) {
    if (widgetResolveFns[mountId]) {
        widgetResolveFns[mountId](widgetView);
    } else {
        widgetPromises[mountId] = Promise.resolve(widgetView);
    }
}

function requestWidget(mountId) {
    if (!widgetPromises[mountId]) {
        widgetPromises[mountId] = new Promise(resolve => widgetResolveFns[mountId] = resolve);
    }
    return widgetPromises[mountId];
}

function getWidgetManager(voila, kernel) {
    try {
        /* voila < 0.1.8 */
        return new voila.WidgetManager(kernel);
    } catch (e) {
        if (e instanceof TypeError) {
            /* voila >= 0.1.8 */
            const context = {
                session: {
                    kernel,
                    kernelChanged: {
                        connect: () => { }
                    },
                    statusChanged: {
                        connect: () => { }
                    },
                },
                saveState: {
                    connect: () => { }
                },
                /* voila >= 0.2.8 */
                sessionContext: {
                    session: {
                        kernel
                    },
                    kernelChanged: {
                        connect: () => {
                        }
                    },
                    statusChanged: {
                        connect: () => {
                        }
                    },
                    connectionStatusChanged: {
                        connect: () => {
                        }
                    },
                },
            };

            const settings = {
                saveState: false
            };

            const rendermime = new voila.RenderMimeRegistry({
                initialFactories: voila.standardRendererFactories
            });

            return new voila.WidgetManager(context, rendermime, settings);
        } else {
            throw e;
        }
    }
}

function injectDebugMessageInterceptor(kernel) {
    const _original_handle_message = kernel._handleMessage.bind(kernel)
    kernel._handleMessage = ((msg) => {
        if (msg.msg_type === 'error') {
            app.$data.voilaDebugMessages.push({
                cell: '_',
                traceback: msg.content.traceback.map(line => ansiSpan(_.escape(line)))
            });
        } else if (msg.msg_type === 'stream' && (msg.content['name'] === 'stdout' || msg.content['name'] === 'stderr')) {
            app.$data.voilaDebugMessages.push({
                cell: '_',
                name: msg.content.name,
                text: msg.content.text
            });
        }
        return _original_handle_message(msg);
    })
}


class WebSocketRedirectWebWorker {
    // redirects to webworker
    constructor(url) {
        console.log('connect url intercepted', url)
        function make_default(name) {
            return () => {
                console.log("default ", name)
            }
        }
        this.onopen = make_default('onopen')
        this.onclose = make_default('onclose')
        this.onmessage = make_default('onmessage')
        setTimeout(() => this.start(), 10)
    }
    send(msg) {
        // console.log('send msg', msg)
        solaraWorker.postMessage({ 'type': 'send', 'value': msg })
    }
    start() {
        solaraWorker.addEventListener('message', async (event) => {
            let msg = event.data
            if (msg.type == 'opened') {
                this.onopen()
            }
            if (msg.type == 'send') {
                this.onmessage({ data: msg.value })
            }
            if (msg.type == 'mount') {
                let model_id = msg.value;

                await solaraMount(model_id)
            }
        });
        solaraWorker.postMessage({ 'type': 'open' })
    }
}


function connectWatchdog() {
    var path = '';
    reloading = false;

    var base = document.baseURI
    if (!base.startsWith('http')) {
        base = window.location.origin + base;
    }
    var WSURL = base.replace("https://", "wss://").replace("http://", "ws://")
    window.wsWatchdog = new WebSocket(WSURL + 'solara/watchdog/' + path);
    wsWatchdog.onopen = () => {
        console.log('connected with watchdog')
    }
    wsWatchdog.onmessage = (evt) => {
        var msg = JSON.parse(evt.data)
        if (msg.type == 'reload') {
            var timeout = 0;
            // if(msg.delay == 'long')
            //     timeout = 1000;
            if (!reloading) {
                reloading = true
                setTimeout(() => {
                    location.reload();
                }, timeout)
            }
        } else if (msg.type == "exception") {
            app.$data.voilaDebugMessages.push({
                cell: '_',
                traceback: ansiSpan(_.escape(msg.traceback))
            });
        }
    }
    wsWatchdog.onclose = () => {
        timeout = 100
        console.log('disconnected watchdog, reconnecting in ', timeout / 1000, 'seconds')
        setTimeout(() => {
            connectWatchdog();
        }, timeout)
    }

}

function getCookiesMap(cookiesString) {
    return cookiesString.split(";")
        .map(function (cookieString) {
            return cookieString.trim().split("=");
        })
        .reduce(function (acc, curr) {
            acc[curr[0]] = curr[1];
            return acc;
        }, {});
}
const COOKIE_KEY_CONTEXT_ID = 'solara-context-id'


async function solaraInit() {
    define("vue", [], () => Vue);
    define("vuetify", [], { framework: app.$vuetify });
    console.log(document.cookie)
    cookies = getCookiesMap(document.cookie);
    const contextId = cookies[COOKIE_KEY_CONTEXT_ID]
    console.log('contextId', contextId)
    connectWatchdog()
    // var path = window.location.pathname.substr(14);
    // NOTE: this file is not transpiled, async/await is the only modern feature we use here
    return new Promise((resolve, reject) => {
        require([window.voila_js_url || 'static/dist/voila.js'], function (voila) {
            window.voila = voila;
            // requirejs doesn't like to be passed an async function, so create one inside
            (async function () {
                if (for_pyodide) {
                    options = { WebSocket: WebSocketRedirectWebWorker }
                } else {
                    options = {}
                }
                window.kernel = await voila.connectKernel('jupyter', null, options)
                if (!kernel) {
                    return;
                }
                const context = {
                    sessionContext: {
                        session: {
                            kernel,
                            kernelChanged: {
                                connect: () => { }
                            },
                        },
                        statusChanged: {
                            connect: () => { }
                        },
                        kernelChanged: {
                            connect: () => { }
                        },
                        connectionStatusChanged: {
                            connect: () => { }
                        },
                    },
                    saveState: {
                        connect: () => { }
                    },
                };

                const settings = {
                    saveState: false
                };

                const rendermime = new voila.RenderMimeRegistry({
                    initialFactories: voila.extendedRendererFactories
                });

                window.widgetManager = new voila.WidgetManager(context, rendermime, settings);
                // it seems if we attach this to early, it will not be called
                const matches = document.cookie.match('\\b_xsrf=([^;]*)\\b');
                const xsrfToken = (matches && matches[1]) || '';
                const configData = JSON.parse(document.getElementById('jupyter-config-data').textContent);
                const baseUrl = 'jupyter';
                // window.addEventListener('beforeunload', function (e) {
                //     const data = new FormData();
                //     data.append("_xsrf", xsrfToken);
                //     // window.navigator.sendBeacon(`${baseUrl}voila/api/shutdown/${kernel.id}`, data);
                //     // kernel.dispose();
                // });
                app.$data.loading_text = 'Loading app';
                await widgetManager.build_widgets();
                voila.renderMathJax();
                resolve()
            })()
        });
    });
}

async function solaraMount(model_id) {
    console.log("will mount", model_id)
    await solaraInitialized;

    async function init() {
        await Promise.all(Object.values(widgetManager._models).map(async (modelPromise) => {
            const model = await modelPromise;
            // console.log(model)
            if (model.model_id == model_id) {
                const view = await widgetManager.create_view(model);
                provideWidget('content', view);
            }
        }));
        app.$data.loadingPercentage = 0;
        app.$data.loading_text = 'Done';
        app.$data.loading = false;
    }
    if (document.readyState === 'complete') {
        init()
    } else {
        window.addEventListener('load', init);
    }
}
