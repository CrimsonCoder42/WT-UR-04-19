import { useState, useEffect } from 'react';


const ACCESS_TOKEN =
    sessionStorage.getItem('token')

const useFetch = (url, method = 'GET', body) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);

            try {
                const token = ACCESS_TOKEN;

                const headers = {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                };

                const options = {
                    method,
                    headers
                };

                if (body) {
                    options.body = body;
                }

                // eslint-disable-next-line
                const response = await fetch(url, {
                    ...options
                });

                if (!response.ok) {
                    throw new Error('Error fetching data');
                }
                // eslint-disable-next-line
                const data = await response.json();
                setData(data);
                // eslint-disable-next-line
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [url, method, body]);

    return { data, loading, error };
};

export default useFetch;
