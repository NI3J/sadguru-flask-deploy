/**
 * Advanced Audio Player for Spiritual Website
 * Features: Playlist, Volume Control, Progress Bar, Shuffle, Repeat
 */

class SpiritualAudioPlayer {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            autoplay: false,
            loop: false,
            shuffle: false,
            volume: 0.8,
            theme: 'spiritual',
            ...options
        };
        
        this.currentTrack = 0;
        this.isPlaying = false;
        this.playlist = [];
        this.audio = new Audio();
        
        this.init();
    }
    
    init() {
        this.createPlayer();
        this.bindEvents();
        this.setupAudio();
    }
    
    createPlayer() {
        const playerHTML = `
            <div class="spiritual-audio-player ${this.options.theme}">
                <div class="player-header">
                    <h3 class="player-title">🕉️ Spiritual Audio Player</h3>
                </div>
                
                <div class="track-info">
                    <div class="track-title">Select a track to play</div>
                    <div class="track-artist"></div>
                </div>
                
                <div class="progress-container">
                    <div class="time-display">
                        <span class="current-time">0:00</span>
                        <span class="total-time">0:00</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                        <div class="progress-handle"></div>
                    </div>
                </div>
                
                <div class="controls">
                    <button class="btn-control btn-shuffle" title="Shuffle">
                        🔀
                    </button>
                    <button class="btn-control btn-prev" title="Previous">
                        ⏮️
                    </button>
                    <button class="btn-control btn-play-pause" title="Play/Pause">
                        ▶️
                    </button>
                    <button class="btn-control btn-next" title="Next">
                        ⏭️
                    </button>
                    <button class="btn-control btn-repeat" title="Repeat">
                        🔁
                    </button>
                </div>
                
                <div class="volume-container">
                    <span class="volume-icon">🔊</span>
                    <input type="range" class="volume-slider" min="0" max="100" value="${this.options.volume * 100}">
                </div>
                
                <div class="playlist-container">
                    <div class="playlist-header">
                        <h4>📜 Playlist</h4>
                        <button class="btn-toggle-playlist">▼</button>
                    </div>
                    <ul class="playlist"></ul>
                </div>
            </div>
        `;
        
        this.container.innerHTML = playerHTML;
        this.getElements();
    }
    
    getElements() {
        this.trackTitle = this.container.querySelector('.track-title');
        this.trackArtist = this.container.querySelector('.track-artist');
        this.currentTimeEl = this.container.querySelector('.current-time');
        this.totalTimeEl = this.container.querySelector('.total-time');
        this.progressBar = this.container.querySelector('.progress-bar');
        this.progressFill = this.container.querySelector('.progress-fill');
        this.progressHandle = this.container.querySelector('.progress-handle');
        this.playPauseBtn = this.container.querySelector('.btn-play-pause');
        this.prevBtn = this.container.querySelector('.btn-prev');
        this.nextBtn = this.container.querySelector('.btn-next');
        this.shuffleBtn = this.container.querySelector('.btn-shuffle');
        this.repeatBtn = this.container.querySelector('.btn-repeat');
        this.volumeSlider = this.container.querySelector('.volume-slider');
        this.volumeIcon = this.container.querySelector('.volume-icon');
        this.playlistEl = this.container.querySelector('.playlist');
        this.togglePlaylistBtn = this.container.querySelector('.btn-toggle-playlist');
    }
    
    bindEvents() {
        // Play/Pause
        this.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        
        // Navigation
        this.prevBtn.addEventListener('click', () => this.previousTrack());
        this.nextBtn.addEventListener('click', () => this.nextTrack());
        
        // Shuffle and Repeat
        this.shuffleBtn.addEventListener('click', () => this.toggleShuffle());
        this.repeatBtn.addEventListener('click', () => this.toggleRepeat());
        
        // Volume
        this.volumeSlider.addEventListener('input', (e) => this.setVolume(e.target.value / 100));
        
        // Progress bar
        this.progressBar.addEventListener('click', (e) => this.seekTo(e));
        
        // Playlist toggle
        this.togglePlaylistBtn.addEventListener('click', () => this.togglePlaylist());
        
        // Audio events
        this.audio.addEventListener('loadedmetadata', () => this.updateDuration());
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('ended', () => this.handleTrackEnd());
        this.audio.addEventListener('error', (e) => this.handleError(e));
    }
    
    setupAudio() {
        this.audio.volume = this.options.volume;
        this.audio.loop = this.options.loop;
    }
    
    // Public Methods
    loadPlaylist(tracks) {
        this.playlist = tracks;
        this.renderPlaylist();
        if (tracks.length > 0) {
            this.loadTrack(0);
        }
    }
    
    addTrack(track) {
        this.playlist.push(track);
        this.renderPlaylist();
    }
    
    removeTrack(index) {
        this.playlist.splice(index, 1);
        this.renderPlaylist();
        if (index === this.currentTrack && this.playlist.length > 0) {
            this.loadTrack(Math.min(this.currentTrack, this.playlist.length - 1));
        }
    }
    
    loadTrack(index) {
        if (index >= 0 && index < this.playlist.length) {
            this.currentTrack = index;
            const track = this.playlist[index];
            
            this.audio.src = track.src;
            this.trackTitle.textContent = track.title;
            this.trackArtist.textContent = track.artist || '';
            
            this.updatePlaylistSelection();
            this.audio.load();
        }
    }
    
    play() {
        if (this.playlist.length === 0) return;
        
        this.audio.play().then(() => {
            this.isPlaying = true;
            this.playPauseBtn.textContent = '⏸️';
        }).catch(e => {
            console.error('Playback failed:', e);
            alert('Audio playback failed. Please interact with the page first.');
        });
    }
    
    pause() {
        this.audio.pause();
        this.isPlaying = false;
        this.playPauseBtn.textContent = '▶️';
    }
    
    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
    
    previousTrack() {
        if (this.options.shuffle) {
            this.loadTrack(Math.floor(Math.random() * this.playlist.length));
        } else {
            const prevIndex = this.currentTrack > 0 ? this.currentTrack - 1 : this.playlist.length - 1;
            this.loadTrack(prevIndex);
        }
        
        if (this.isPlaying) {
            this.play();
        }
    }
    
    nextTrack() {
        if (this.options.shuffle) {
            this.loadTrack(Math.floor(Math.random() * this.playlist.length));
        } else {
            const nextIndex = this.currentTrack < this.playlist.length - 1 ? this.currentTrack + 1 : 0;
            this.loadTrack(nextIndex);
        }
        
        if (this.isPlaying) {
            this.play();
        }
    }
    
    toggleShuffle() {
        this.options.shuffle = !this.options.shuffle;
        this.shuffleBtn.style.backgroundColor = this.options.shuffle ? '#c28800' : '';
    }
    
    toggleRepeat() {
        this.options.loop = !this.options.loop;
        this.audio.loop = this.options.loop;
        this.repeatBtn.style.backgroundColor = this.options.loop ? '#c28800' : '';
    }
    
    setVolume(volume) {
        this.audio.volume = volume;
        this.options.volume = volume;
        
        // Update volume icon
        if (volume === 0) {
            this.volumeIcon.textContent = '🔇';
        } else if (volume < 0.5) {
            this.volumeIcon.textContent = '🔉';
        } else {
            this.volumeIcon.textContent = '🔊';
        }
    }
    
    seekTo(event) {
        const rect = this.progressBar.getBoundingClientRect();
        const percent = (event.clientX - rect.left) / rect.width;
        const newTime = percent * this.audio.duration;
        
        if (!isNaN(newTime)) {
            this.audio.currentTime = newTime;
        }
    }
    
    // Private Methods
    renderPlaylist() {
        this.playlistEl.innerHTML = '';
        
        this.playlist.forEach((track, index) => {
            const li = document.createElement('li');
            li.className = 'playlist-item';
            li.innerHTML = `
                <div class="track-number">${index + 1}</div>
                <div class="track-details">
                    <div class="track-name">${track.title}</div>
                    <div class="track-artist">${track.artist || ''}</div>
                </div>
                <div class="track-duration">${track.duration || ''}</div>
            `;
            
            li.addEventListener('click', () => {
                this.loadTrack(index);
                if (this.isPlaying) {
                    this.play();
                }
            });
            
            this.playlistEl.appendChild(li);
        });
    }
    
    updatePlaylistSelection() {
        this.container.querySelectorAll('.playlist-item').forEach((item, index) => {
            item.classList.toggle('active', index === this.currentTrack);
        });
    }
    
    updateDuration() {
        this.totalTimeEl.textContent = this.formatTime(this.audio.duration);
    }
    
    updateProgress() {
        const progress = (this.audio.currentTime / this.audio.duration) * 100;
        this.progressFill.style.width = `${progress}%`;
        this.currentTimeEl.textContent = this.formatTime(this.audio.currentTime);
    }
    
    handleTrackEnd() {
        if (this.options.loop) {
            this.play();
        } else {
            this.nextTrack();
        }
    }
    
    handleError(error) {
        console.error('Audio error:', error);
        this.trackTitle.textContent = 'Error loading audio';
    }
    
    togglePlaylist() {
        const playlist = this.playlistEl;
        const isVisible = playlist.style.display !== 'none';
        
        playlist.style.display = isVisible ? 'none' : 'block';
        this.togglePlaylistBtn.textContent = isVisible ? '▼' : '▲';
    }
    
    formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
}

// CSS Styles (add to your CSS file)
const playerStyles = `
.spiritual-audio-player {
    background: linear-gradient(135deg, #fff8dc, #f0e68c);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    max-width: 500px;
    margin: 20px auto;
    font-family: 'Tiro Devanagari Marathi', serif;
}

.player-header .player-title {
    text-align: center;
    color: #5c3d00;
    margin: 0 0 20px 0;
}

.track-info {
    text-align: center;
    margin-bottom: 20px;
}

.track-title {
    font-size: 1.2em;
    font-weight: bold;
    color: #5c3d00;
}

.track-artist {
    color: #8b7355;
    font-size: 0.9em;
}

.progress-container {
    margin-bottom: 20px;
}

.time-display {
    display: flex;
    justify-content: space-between;
    font-size: 0.8em;
    color: #666;
    margin-bottom: 5px;
}

.progress-bar {
    height: 6px;
    background: #ddd;
    border-radius: 3px;
    position: relative;
    cursor: pointer;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #c28800, #ffd700);
    border-radius: 3px;
    transition: width 0.1s;
}

.controls {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-bottom: 20px;
}

.btn-control {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
    padding: 8px;
    border-radius: 50%;
    transition: background 0.3s;
}

.btn-control:hover {
    background: rgba(194, 136, 0, 0.2);
}

.volume-container {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
}

.volume-slider {
    flex: 1;
    height: 4px;
    background: #ddd;
    border-radius: 2px;
    outline: none;
}

.playlist-container {
    border-top: 1px solid #ddd;
    padding-top: 15px;
}

.playlist-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.btn-toggle-playlist {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.2em;
}

.playlist {
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 200px;
    overflow-y: auto;
}

.playlist-item {
    display: flex;
    align-items: center;
    padding: 8px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s;
}

.playlist-item:hover {
    background: rgba(194, 136, 0, 0.1);
}

.playlist-item.active {
    background: rgba(194, 136, 0, 0.3);
}

.track-number {
    width: 30px;
    text-align: center;
    color: #666;
}

.track-details {
    flex: 1;
    margin-left: 10px;
}

.track-name {
    font-weight: bold;
    color: #5c3d00;
}

.track-duration {
    color: #666;
    font-size: 0.8em;
}

@media (max-width: 480px) {
    .spiritual-audio-player {
        padding: 15px;
        margin: 10px;
    }
    
    .controls {
        gap: 10px;
    }
    
    .btn-control {
        font-size: 1.3em;
        padding: 6px;
    }
}
`;

// Add styles to document
if (!document.getElementById('spiritual-audio-player-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'spiritual-audio-player-styles';
    styleSheet.textContent = playerStyles;
    document.head.appendChild(styleSheet);
}

// Export for use
window.SpiritualAudioPlayer = SpiritualAudioPlayer;