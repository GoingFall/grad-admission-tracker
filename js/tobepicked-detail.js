// 待选择项目详情页功能
let projectData = null;
let socialMediaData = null;

// 从URL获取项目ID
function getProjectIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// 加载项目数据
async function loadProjectData() {
    const projectId = getProjectIdFromUrl();
    
    if (!projectId) {
        showError('缺少项目ID参数');
        return;
    }

    try {
        // 加载项目基本信息
        const projectsResponse = await fetch('data/tobepicked-projects.json');
        if (!projectsResponse.ok) {
            throw new Error('无法加载项目数据');
        }
        const projects = await projectsResponse.json();
        projectData = projects.find(p => p.id === projectId);

        if (!projectData) {
            showError('未找到该项目');
            return;
        }

        // 加载社交媒体数据（暂时留空，后续补充）
        // try {
        //     const socialResponse = await fetch('data/tobepicked-social-media.json');
        //     if (socialResponse.ok) {
        //         socialMediaData = await socialResponse.json();
        //     }
        // } catch (error) {
        //     console.warn('加载社交媒体数据失败:', error);
        // }

        renderProjectDetail();
    } catch (error) {
        console.error('加载数据失败:', error);
        showError('加载数据失败，请刷新页面重试。');
    }
}

// 显示错误信息
function showError(message) {
    document.getElementById('loading').style.display = 'none';
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// 渲染项目详情
function renderProjectDetail() {
    document.getElementById('loading').style.display = 'none';
    const detailDiv = document.getElementById('project-detail');
    detailDiv.style.display = 'block';

    // 渲染基本信息
    document.getElementById('project-title').textContent = projectData.project_name;
    document.getElementById('project-university').textContent = projectData.university;
    document.getElementById('project-english-name').textContent = projectData.english_name;
    
    const admissionRateEl = document.getElementById('project-admission-rate');
    admissionRateEl.textContent = projectData.admission_rate || '待查询';
    admissionRateEl.className = `admission-rate low`; // 待选择项目默认使用low样式
    
    document.getElementById('project-important-date').textContent = projectData.important_date || '待定';
    document.getElementById('project-deadline').textContent = projectData.deadline || '待查询';
    document.getElementById('project-ielts').textContent = projectData.ielts_requirement || '无要求';
    document.getElementById('project-tuition').textContent = projectData.tuition || '待查询';
    document.getElementById('project-duration').textContent = projectData.duration || '待查询';
    document.getElementById('project-requirements').textContent = projectData.requirements || '待查询';
    document.getElementById('project-description').textContent = projectData.description || '暂无描述';
    
    const urlEl = document.getElementById('project-url');
    urlEl.href = projectData.url || '#';
    urlEl.textContent = projectData.url || '暂无链接';

    // 渲染社交媒体信息（暂时留空）
    // if (socialMediaData && socialMediaData[projectData.id]) {
    //     renderSocialMedia(socialMediaData[projectData.id]);
    // }
}

// 渲染社交媒体信息（预留，后续补充）
function renderSocialMedia(data) {
    const section = document.getElementById('social-media-section');
    section.style.display = 'block';

    // 渲染小红书帖子
    if (data.xiaohongshu_posts && data.xiaohongshu_posts.length > 0) {
        const xhsSection = document.getElementById('xiaohongshu-section');
        xhsSection.style.display = 'block';
        const xhsContainer = document.getElementById('xiaohongshu-posts');
        xhsContainer.innerHTML = data.xiaohongshu_posts.map(post => `
            <div class="post-item">
                <div class="post-title">
                    ${post.title}
                </div>
                <div class="post-meta">
                    <span>发布时间：${post.publish_date}</span>
                    <span>作者：${post.author}</span>
                    <span>点赞数：${post.likes}</span>
                </div>
            </div>
        `).join('');
    }

    // 渲染知乎帖子
    if (data.zhihu_posts && data.zhihu_posts.length > 0) {
        const zhihuSection = document.getElementById('zhihu-section');
        zhihuSection.style.display = 'block';
        const zhihuContainer = document.getElementById('zhihu-posts');
        zhihuContainer.innerHTML = data.zhihu_posts.map(post => `
            <div class="post-item">
                <div class="post-title">
                    <a href="${post.url}" target="_blank" rel="noopener noreferrer">${post.title}</a>
                </div>
                <div class="post-meta">
                    <span>发布时间：${post.publish_date}</span>
                    <span>点赞数：${post.likes}</span>
                    <span>回答数：${post.answers}</span>
                </div>
                ${post.summary ? `<div class="post-summary">${post.summary}</div>` : ''}
            </div>
        `).join('');
    }

    // 渲染关键信息总结
    if (data.summary && Object.keys(data.summary).length > 0) {
        const summarySection = document.getElementById('summary-section');
        summarySection.style.display = 'block';
        const summaryContent = document.getElementById('summary-content');
        summaryContent.innerHTML = Object.entries(data.summary).map(([key, value]) => `
            <h5>${key}</h5>
            <div>${formatSummaryText(value)}</div>
        `).join('');
    }
}

// 格式化总结文本
function formatSummaryText(text) {
    if (!text) return '';
    // 将换行符转换为HTML换行
    return text.split('\n').map(line => {
        line = line.trim();
        if (!line) return '';
        // 处理列表项
        if (line.match(/^\d+\./)) {
            return `<p>${line}</p>`;
        }
        return `<p>${line}</p>`;
    }).join('');
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadProjectData();
});

