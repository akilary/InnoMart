/** Выполняет HTTP-запрос и возвращает JSON ответ */
export async function fetchApi(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json",
                ...options.headers
            },
            credentials: "include"
        });

        if (response.status === 401) {
            window.location.href = "/auth/register";
            return;
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || `Ошибка запроса: ${response.status}`);
        }

        return await data;
    } catch (error) {
        console.error(`%c[API] Ошибка при запросе ${url}:`, 'color: red; font-weight: bold;', error);
        throw error;
    }
}