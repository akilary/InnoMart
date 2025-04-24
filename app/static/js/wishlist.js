import { fetchApi } from './utils/api.js';

function initWishlist() {
    // Удаление из избранного
    const deleteButtons = document.querySelectorAll('.button--remove-favorite');
    deleteButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const productId = button.dataset.productId;
            try {
                await fetchApi(`/api/wishlist/${productId}`, { method: 'DELETE' });
                console.log('Товар удалён');
                button.closest('.favorites__item').remove();
            } catch (error) {
                console.error('Ошибка при удалении товара');
            }
        });
    });

    // Добавление в избранное
    document.body.addEventListener('click', async (e) => {
        const button = e.target.closest('.wishlist-btn');
        const is_button_favorite = e.target.closest('.button--remove-favorite');
        if (!button || is_button_favorite) return;

        e.preventDefault();
        const productId = button.dataset.productId;
        const icon = button.querySelector('i.material-icons');

        try {
            await fetchApi(`/api/wishlist/${productId}`, { method: 'PUT' });
            button.classList.toggle('active');
            if (icon) {
                icon.textContent = icon.textContent.trim() === 'bookmark' ? 'bookmark_add' : 'bookmark';
            }
        } catch (error) {
            console.error('Ошибка при добавлении в избранное');
        }
    });
}

document.addEventListener('DOMContentLoaded', initWishlist);