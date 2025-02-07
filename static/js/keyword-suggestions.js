document.addEventListener('DOMContentLoaded', function() {
    const keywordInput = document.getElementById('keywordInput');
    const searchButton = document.getElementById('searchKeywords');
    const keywordsResult = document.getElementById('keywordsResult');
    const keywordsList = keywordsResult.querySelector('.keywords-list');
    const loadingIndicator = keywordsResult.querySelector('.keywords-loading');

    // Функция для показа индикатора загрузки
    function showLoading() {
        loadingIndicator.classList.remove('d-none');
        keywordsList.innerHTML = '';
    }

    // Функция для скрытия индикатора загрузки
    function hideLoading() {
        loadingIndicator.classList.add('d-none');
    }

    // Функция для отображения ключевых слов
    function displayKeywords(keywords) {
        keywordsList.innerHTML = '';
        keywords.forEach((keyword, index) => {
            const delay = index * 100; // Задержка для анимации
            const keywordItem = document.createElement('div');
            keywordItem.className = 'keyword-item';
            keywordItem.style.animationDelay = `${delay}ms`;
            keywordItem.innerHTML = `
                <div class="keyword-text">${keyword.text}</div>
                <div class="keyword-metrics">
                    <span class="me-2">
                        <i class="fas fa-search"></i> ${keyword.volume}
                    </span>
                    <span>
                        <i class="fas fa-chart-line"></i> ${keyword.difficulty}
                    </span>
                </div>
            `;
            keywordsList.appendChild(keywordItem);
        });
    }

    // Обработчик поиска ключевых слов
    searchButton.addEventListener('click', async function() {
        const query = keywordInput.value.trim();
        if (!query) return;

        showLoading();

        try {
            // Здесь будет запрос к серверу для получения ключевых слов
            // Пока используем тестовые данные
            await new Promise(resolve => setTimeout(resolve, 1500)); // Имитация задержки запроса
            
            const mockKeywords = [
                { text: query + " услуги", volume: "1,200", difficulty: "Средняя" },
                { text: query + " цена", volume: "890", difficulty: "Низкая" },
                { text: query + " заказать", volume: "750", difficulty: "Средняя" },
                { text: query + " стоимость", volume: "670", difficulty: "Низкая" },
                { text: query + " онлайн", volume: "560", difficulty: "Высокая" },
                { text: query + " отзывы", volume: "450", difficulty: "Средняя" },
                { text: "купить " + query, volume: "890", difficulty: "Высокая" },
                { text: "заказать " + query, volume: "670", difficulty: "Средняя" },
            ];

            displayKeywords(mockKeywords);
        } catch (error) {
            keywordsList.innerHTML = `
                <div class="alert alert-danger">
                    Произошла ошибка при поиске ключевых слов. Пожалуйста, попробуйте позже.
                </div>
            `;
        } finally {
            hideLoading();
        }
    });

    // Обработка нажатия Enter в поле ввода
    keywordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchButton.click();
        }
    });
});
