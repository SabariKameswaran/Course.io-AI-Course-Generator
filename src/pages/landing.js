import React, { useEffect } from 'react';
import Header from '../components/header';
import SlideOne from '../components/landing/slideOne';
import { serverURL } from '../constants';
import axios from 'axios';

const Landing = () => {

    useEffect(() => {
        async function dashboardData() {
            const postURL = serverURL + `/api/policies`;
            const response = await axios.get(postURL);
            sessionStorage.setItem('TermsPolicy', response.data[0].terms);
            sessionStorage.setItem('PrivacyPolicy', response.data[0].privacy)
        }
        if (sessionStorage.getItem('TermsPolicy') === null && sessionStorage.getItem('PrivacyPolicy') === null) {
            dashboardData();
        }
    }, []);

    return (
        <>
            <Header isHome={false} />
            <SlideOne />
        </>
    );
};

export default Landing;