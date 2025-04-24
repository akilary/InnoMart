/**
 * Выполняет HTTP-запрос и возвращает JSON ответ
 */
export async function fetchApi(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                ...options.headers
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`%c[API] Ошибка при запросе ${url}:`, 'color: red; font-weight: bold;', error);
        throw error;
    }
}
