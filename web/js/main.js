// 列表页功能
let projects = [];
let sortedProjects = [];

// 加载项目数据
async function loadProjects() {
    try {
        const response = await fetch('data/projects.json');
        if (!response.ok) {
            throw new Error('无法加载项目数据');
        }
        projects = await response.json();
        sortedProjects = [...projects];
        renderProjects();
        updateProjectCount();
    } catch (error) {
        console.error('加载数据失败:', error);
        document.getElementById('projects-container').innerHTML = 
            '<div class="error">加载数据失败，请刷新页面重试。</div>';
    }
}

// 渲染项目卡片
function renderProjects() {
    const container = document.getElementById('projects-container');
    
    if (sortedProjects.length === 0) {
        container.innerHTML = '<div class="error">暂无项目数据</div>';
        return;
    }

    container.innerHTML = sortedProjects.map(project => `
        <div class="project-card" onclick="goToDetail('${project.id}')">
            <div class="project-card-header">
                <div>
                    <div class="project-card-title">${project.project_name}</div>
                    <div class="project-card-university">${project.university}</div>
                </div>
                <div class="admission-rate-badge ${getAdmissionRateClass(project.admission_rate)}">
                    ${project.admission_rate}
                </div>
            </div>
            <div class="project-card-info">
                <div class="info-item">
                    <strong>重要日期：</strong>
                    <span>${project.important_date || '待定'}</span>
                </div>
                <div class="info-item">
                    <strong>截止日期：</strong>
                    <span>${project.deadline || '待查询'}</span>
                </div>
                <div class="info-item">
                    <strong>项目时长：</strong>
                    <span>${project.duration || '待查询'}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// 获取录取概率样式类
function getAdmissionRateClass(rate) {
    if (!rate) return 'low';
    const num = parseInt(rate);
    if (num >= 60) return 'high';
    if (num >= 30) return 'medium';
    return 'low';
}

// 排序功能
function sortProjects(sortType) {
    sortedProjects = [...projects];
    
    switch (sortType) {
        case 'admission_rate_desc':
            sortedProjects.sort((a, b) => {
                const rateA = parseInt(a.admission_rate) || 0;
                const rateB = parseInt(b.admission_rate) || 0;
                return rateB - rateA;
            });
            break;
        case 'admission_rate_asc':
            sortedProjects.sort((a, b) => {
                const rateA = parseInt(a.admission_rate) || 0;
                const rateB = parseInt(b.admission_rate) || 0;
                return rateA - rateB;
            });
            break;
        case 'university':
            sortedProjects.sort((a, b) => {
                return a.university.localeCompare(b.university, 'zh-CN');
            });
            break;
        case 'deadline':
            sortedProjects.sort((a, b) => {
                // 简单的日期比较，提取年份和月份
                const dateA = extractDate(a.deadline);
                const dateB = extractDate(b.deadline);
                if (!dateA && !dateB) return 0;
                if (!dateA) return 1;
                if (!dateB) return -1;
                return dateA.localeCompare(dateB);
            });
            break;
        default:
            break;
    }
    
    renderProjects();
}

// 提取日期用于排序
function extractDate(dateStr) {
    if (!dateStr || dateStr === '待查询') return null;
    // 尝试提取年份和月份
    const match = dateStr.match(/(\d{4})[年-](\d{1,2})/);
    if (match) {
        const year = match[1];
        const month = match[2].padStart(2, '0');
        return `${year}-${month}`;
    }
    return dateStr;
}

// 更新项目数量
function updateProjectCount() {
    const countElement = document.getElementById('project-count');
    if (countElement) {
        countElement.innerHTML = `共 <strong>${sortedProjects.length}</strong> 个项目`;
    }
}

// 跳转到详情页
function goToDetail(projectId) {
    window.location.href = `detail.html?id=${encodeURIComponent(projectId)}`;
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    
    // 绑定排序选择器事件
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            sortProjects(e.target.value);
        });
    }
});

