import axios from 'axios';
import {returnErrors} from './messages';
import {EVENTS_ERROR, EVENTS_LOADED, EVENTS_LOADING} from "./types";

export const loadEvents = (categoryId) => (dispatch, getState) => {
    dispatch({type: EVENTS_LOADING});
    axios.get(`api/events/category/${categoryId}`)
        .then(res => {
            dispatch({
                type: EVENTS_LOADED,
                payload: res.data
            })
        })
        .catch(err => {
            dispatch(returnErrors(err.response.data, err.response.status));
            dispatch({
                type: EVENTS_ERROR
            });
        })
};