// Obtener el ID de la receta de Jinja2
const RECIPE_ID = {{ recipe.id }}; 
const COMMENTS_KEY = `forum_recipe_${RECIPE_ID}`;
const commentsContainer = document.getElementById('commentsContainer');
const commentForm = document.getElementById('commentForm');

function loadComments() {
    commentsContainer.innerHTML = '';
    const comments = JSON.parse(localStorage.getItem(COMMENTS_KEY)) || [];

    if (comments.length === 0) {
        commentsContainer.innerHTML = '<p class="text-muted">Sé el primero en dejar un comentario o recomendación.</p>';
        return;
    }

    // Mostrar los mensajes
    comments.forEach(comment => {
        const date = new Date(comment.timestamp);
        const relativeTime = getRelativeTime(date); // Función auxiliar para mejor UX

        commentsContainer.innerHTML += `
            <div class="comment mb-3 p-3 border rounded bg-white shadow-sm">
                <p class="mb-1"><strong>${comment.user}:</strong> ${comment.text}</p>
                <small class="text-muted">${relativeTime}</small>
            </div>
        `;
    });
}

function saveComment(event) {
    event.preventDefault(); // Evita que el formulario recargue la página

    const user = document.getElementById('userName').value.trim();
    const text = document.getElementById('commentText').value.trim();

    if (user && text) {
        const comments = JSON.parse(localStorage.getItem(COMMENTS_KEY)) || [];
        
        // Añadir el nuevo comentario
        comments.unshift({ // unshift añade al inicio para que el más nuevo salga primero
            user: user,
            text: text,
            timestamp: new Date().toISOString()
        });

        // Guardar en localStorage
        localStorage.setItem(COMMENTS_KEY, JSON.stringify(comments));

        // Recargar comentarios y limpiar formulario
        loadComments();
        document.getElementById('userName').value = '';
        document.getElementById('commentText').value = '';
    }
}

// Función auxiliar para mostrar el tiempo de forma amigable (opcional, mejora la UX)
function getRelativeTime(date) {
    const diff = new Date() - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (seconds < 60) return `hace unos segundos`;
    if (minutes < 60) return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
    if (hours < 24) return `hace ${hours} hora${hours > 1 ? 's' : ''}`;
    if (days < 30) return `hace ${days} día${days > 1 ? 's' : ''}`;
    return date.toLocaleDateString();
}

// --- Event Listeners y Carga Inicial ---
commentForm.addEventListener('submit', saveComment);
loadComments();
