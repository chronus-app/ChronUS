import Vue from 'vue';

const state = {
    token: localStorage.getItem('token') || null
}

const getters = {
    loggedIn(state) {
        return state.token != null;
    }
}

const actions = {
    retrieveToken(context, credentials) {
        return new Promise((resolve, reject) => {
            Vue.http.post('token/', 
                {
                    email: credentials.email,
                    password: credentials.password    
                }
            ).then(response => {
                const token = response.body.token;
                localStorage.setItem('token', token);
                context.commit('setToken', token);
                resolve(response);
            }).catch(error => {
                reject(error);
            });
        });
        
    },
    destroyToken(context) {
        return new Promise((resolve, reject) => {
            Vue.http.get('logout/',
                {
                    headers: {
                        'Authorization': `Token ${context.state.token}`
                    }
                }
            )
            .then(response => {
                localStorage.removeItem('token');
                context.commit('destroyToken');
                resolve(response);
            }).catch(error => {
                reject(error);
            });
        });
    }
}

const mutations = {
    setToken(state, token) {
        state.token = token;
    },
    destroyToken(state) {
        state.token = null;
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}