// Fonctions utilitaires
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function showNotification(message, type = 'success', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span class="notification-message">${message}</span>
        <button class="notification-close">&times;</button>
    `;
    document.body.appendChild(notification);
    
    // Force le reflow pour assurer que la transition fonctionne
    notification.offsetHeight;
    
    notification.classList.add('show');
    
    notification.querySelector('.notification-close').addEventListener('click', function() {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    });
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

function formatDate(date) {
    const options = { day: 'numeric', month: 'short', year: 'numeric' };
    return new Date(date).toLocaleDateString('fr-FR', options);
}

// Gestionnaire d'erreurs AJAX
function handleAjaxError(error) {
    console.error('Erreur AJAX:', error);
    showNotification(
        'Une erreur est survenue lors de la communication avec le serveur.',
        'error'
    );
}

// Initialisation des gestionnaires d'événements
document.addEventListener('DOMContentLoaded', function() {
    initCommentActions();
    
    // Gestionnaire pour le bouton "Répondre"
    document.querySelectorAll('.btn-primary').forEach(btn => {
        if (btn.textContent.trim() === 'Répondre') {
            btn.addEventListener('click', function(e) {
                showNotification('Fonctionnalité de réponse activée.', 'info');
            });
        }
    });
    
    // Gestionnaire pour le menu déroulant des commentaires
    document.addEventListener('click', function(e) {
        if (e.target.closest('.dropdown-toggle')) {
            const menu = e.target.closest('.dropdown-toggle').nextElementSibling;
            toggleDropdownMenu(menu);
        } else {
            // Fermer tous les menus si on clique ailleurs
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });
    
    // Formulaire d'ajout de commentaire principal
    const commentForm = document.getElementById('ajax-comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitComment();
        });
    }
});

function toggleDropdownMenu(menu) {
    // Fermer tous les autres menus
    document.querySelectorAll('.dropdown-menu').forEach(item => {
        if (item !== menu) {
            item.style.display = 'none';
        }
    });
    
    // Basculer l'affichage du menu actuel
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

function initCommentActions() {
    // Gestionnaire pour le bouton Modifier
    document.querySelectorAll('.edit-comment').forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-id');
            showEditForm(commentId);
        });
    });
    
    // Gestionnaire pour le bouton Supprimer
    document.querySelectorAll('.delete-comment').forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-id');
            if (confirm('Êtes-vous sûr de vouloir supprimer ce commentaire ?')) {
                deleteComment(commentId);
            }
        });
    });
    
    // Gestionnaire pour le bouton Modifier dans la modal
    document.getElementById('btn-modifier')?.addEventListener('click', function() {
        const commentId = document.getElementById('comment-id-to-update').value;
        const content = document.getElementById('comment-content-edit').value;
        updateComment(commentId, content);
    });
    
    // Gestionnaire pour le bouton Supprimer dans la modal
    document.getElementById('btn-supprimer')?.addEventListener('click', function() {
        const commentId = document.getElementById('comment-id-to-delete').value;
        deleteComment(commentId);
    });
}

function submitComment() {
    const bodyElement = document.getElementById('ajax-body');
    const body = bodyElement.value.trim();
    
    if (!body) {
        showNotification('Le commentaire ne peut pas être vide.', 'error');
        return;
    }
    
    const postId = getPostIdFromUrl();
    const name = document.getElementById('ajax-name')?.value || 'Anonyme';
    const email = document.getElementById('ajax-email')?.value || 'anonyme@example.com';
    
    const data = {
        action: 'add',
        post_id: postId,
        content: body,
        name: name,
        email: email
    };
    
    fetch('/blog/comment/action/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => Promise.reject(data.message || 'Erreur serveur'));
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Ajouter le nouveau commentaire à la liste
            addCommentToDOM(data.comment);
            
            // Réinitialiser le formulaire
            bodyElement.value = '';
            
            // Afficher une notification
            showNotification('Votre commentaire a été ajouté avec succès.', 'success');
            
            // Mettre à jour le compteur de commentaires
            updateCommentCount(1);
        } else {
            showNotification(data.message || 'Erreur lors de l\'ajout du commentaire.', 'error');
        }
    })
    .catch(error => {
        handleAjaxError(error);
    });
}

function showEditForm(commentId) {
    const commentElement = document.getElementById(`comment-${commentId}`);
    const commentBody = commentElement.querySelector('.comment-body');
    const commentText = commentBody.textContent.trim();
    
    // Créer un formulaire d'édition
    const editForm = document.createElement('div');
    editForm.className = 'edit-form';
    editForm.innerHTML = `
        <textarea class="edit-textarea">${commentText}</textarea>
        <div class="edit-actions">
            <button class="btn-cancel">Annuler</button>
            <button class="btn-save">Enregistrer</button>
        </div>
    `;
    
    // Cacher le contenu original et afficher le formulaire
    commentBody.style.display = 'none';
    commentElement.insertBefore(editForm, commentBody.nextSibling);
    
    // Gestionnaire pour le bouton Annuler
    editForm.querySelector('.btn-cancel').addEventListener('click', function() {
        commentBody.style.display = 'block';
        editForm.remove();
    });
    
    // Gestionnaire pour le bouton Enregistrer
    editForm.querySelector('.btn-save').addEventListener('click', function() {
        const newContent = editForm.querySelector('.edit-textarea').value.trim();
        updateComment(commentId, newContent);
    });
    
    // Mettre le focus sur le textarea
    editForm.querySelector('.edit-textarea').focus();
}

function updateComment(commentId, content) {
    if (!content) {
        showNotification('Le commentaire ne peut pas être vide.', 'error');
        return;
    }
    
    const data = {
        action: 'edit',
        comment_id: commentId,
        content: content
    };
    
    fetch('/blog/comment/action/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => Promise.reject(data.message || 'Erreur serveur'));
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Mettre à jour le contenu du commentaire
            const commentElement = document.getElementById(`comment-${commentId}`);
            const commentBody = commentElement.querySelector('.comment-body');
            commentBody.textContent = data.comment.body;
            commentBody.style.display = 'block';
            
            // Supprimer le formulaire d'édition
            const editForm = commentElement.querySelector('.edit-form');
            if (editForm) {
                editForm.remove();
            }
            
            // Fermer la modal si elle existe
            const modal = document.getElementById('editModal');
            if (modal) {
                // Utilisez la fonction de fermeture de modal appropriée selon votre framework
                // Par exemple, pour Bootstrap:
                // $('#editModal').modal('hide');
            }
            
            // Afficher une notification
            showNotification('Votre commentaire a été mis à jour avec succès.', 'success');
        } else {
            showNotification(data.message || 'Erreur lors de la mise à jour du commentaire.', 'error');
        }
    })
    .catch(error => {
        handleAjaxError(error);
    });
}

function deleteComment(commentId) {
    const data = {
        action: 'delete',
        comment_id: commentId
    };
    
    fetch('/blog/comment/action/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => Promise.reject(data.message || 'Erreur serveur'));
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Supprimer le commentaire du DOM
            const commentElement = document.getElementById(`comment-${commentId}`);
            commentElement.classList.add('fade-out');
            
            setTimeout(() => {
                commentElement.remove();
                
                // Mettre à jour le compteur de commentaires
                updateCommentCount(-1);
                
                // Afficher une notification
                showNotification('Votre commentaire a été supprimé avec succès.', 'success');
            }, 300);
            
            // Fermer la modal si elle existe
            const modal = document.getElementById('deleteModal');
            if (modal) {
                // Utilisez la fonction de fermeture de modal appropriée selon votre framework
                // Par exemple, pour Bootstrap:
                // $('#deleteModal').modal('hide');
            }
        } else {
            showNotification(data.message || 'Erreur lors de la suppression du commentaire.', 'error');
        }
    })
    .catch(error => {
        handleAjaxError(error);
    });
}

function addCommentToDOM(comment) {
    const commentsList = document.querySelector('.comments-list');
    if (!commentsList) return;
    
    const newComment = document.createElement('div');
    newComment.className = 'comment';
    newComment.id = `comment-${comment.id}`;
    
    // Déterminer si c'est l'utilisateur actuel qui a écrit le commentaire
    const isOwner = comment.is_owner;
    
    newComment.innerHTML = `
        <div class="comment-header">
            <span class="comment-author">${comment.name}</span>
            <span class="comment-date">${formatDate(comment.created)}</span>
            ${isOwner ? `
                <div class="dropdown">
                    <button class="dropdown-toggle" aria-label="Menu actions">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="5" r="1"></circle>
                            <circle cx="12" cy="12" r="1"></circle>
                            <circle cx="12" cy="19" r="1"></circle>
                        </svg>
                    </button>
                    <div class="dropdown-menu">
                        <button class="dropdown-item edit-comment" data-id="${comment.id}">Modifier</button>
                        <button class="dropdown-item delete-comment" data-id="${comment.id}">Supprimer</button>
                    </div>
                </div>
            ` : ''}
        </div>
        <div class="comment-body">${comment.body}</div>
        <div class="comment-footer">
            <button class="reply-toggle btn-primary" data-parent="${comment.id}">Répondre</button>
        </div>
    `;
    
    // Ajouter le commentaire au début de la liste
    if (commentsList.firstChild) {
        commentsList.insertBefore(newComment, commentsList.firstChild);
    } else {
        commentsList.appendChild(newComment);
    }
    
    // Ajouter les gestionnaires d'événements au nouveau commentaire
    initCommentActions();
}

function updateCommentCount(change) {
    const countElement = document.querySelector('.comments-count');
    if (countElement) {
        let count = parseInt(countElement.textContent.match(/\d+/)[0], 10) || 0;
        count += change;
        
        // Mettre à jour le texte du compteur
        countElement.textContent = `Commentaires (${count})`;
        
        // Si c'est le dernier commentaire et qu'il est supprimé, afficher un message
        if (count === 0) {
            const commentsList = document.querySelector('.comments-list');
            commentsList.innerHTML = '<p>Aucun commentaire pour l\'instant. Soyez le premier à commenter !</p>';
        }
    }
}

function getPostIdFromUrl() {
    // Extraire l'ID du post de l'URL ou d'un élément de la page
    // Exemple : pour une URL comme /blog/post/123-mon-article/
    const match = window.location.pathname.match(/\/post\/(\d+)-/);
    if (match && match[1]) {
        return match[1];
    }
    
    // Sinon, essayer de trouver un élément avec l'ID du post
    const postIdElement = document.getElementById('post-id');
    if (postIdElement) {
        return postIdElement.value;
    }
    
    // Dernier recours: chercher dans les balises meta
    const metaPostId = document.querySelector('meta[name="post-id"]');
    if (metaPostId) {
        return metaPostId.getAttribute('content');
    }
    
    return null;
} 