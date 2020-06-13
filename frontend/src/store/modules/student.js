import Vue from 'vue';

const actions = {
    retrieveLoggedStudent(context) {
        return new Promise((resolve, reject) => {
            Vue.http.get('students/me/',
                {
                    headers: {
                        'Authorization': `Token ${this.state.auth.token}`
                    }
                } 
            ).then(response => {
                resolve(response);
            }).catch(error => {
                reject(error);
            });
        });
    }
}

export default {
    actions
}