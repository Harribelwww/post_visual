function sci_plot(plotType, colorScheme, plot_title, plot_xlabel, plot_ylabel, varargin)
% 参数校验
nGroups = numel(varargin)/2;
if mod(nGroups,1) ~= 0
    error('参数错误：输入参数应为5+3n格式 (n=数据组数)');
end
nGroups = fix(nGroups);

% 创建颜色方案
colors = [];
switch colorScheme
    case 1  % Furina
        colors = [20  21  33;       % 深海蓝
                45  60 129;       % 普鲁士蓝
               147 117  98;       % 陶土棕
                78 164 239;       % 天空蓝
               218 226 237] / 255;% 冰蓝
    case 2  % Nilou
        colors = [20  54  95;       % 深蓝
               214  79  56;       % 赤陶红
               118 162 185;       % 灰蓝
               191 217 229] / 255;% 淡蓝
    otherwise
        colors = get(groot, 'DefaultAxesColorOrder');
end

% 创建图形窗口
fig = figure('Units','centimeters', 'Position',[3 3 16 12],...
             'Color','w', 'InvertHardcopy','off', 'Resize','off');

% 创建坐标轴系统
ax = axes(fig, 'Position',[0.15 0.15 0.75 0.75],...
          'FontName','Times New Roman', 'FontSize',12,...
          'FontWeight','bold', 'LineWidth',0.8,...
          'TickDir','out', 'TickLength',[0.015 0.015],...
          'XColor',[0 0 0], 'YColor',[0 0 0],...
          'Box','on', 'GridLineStyle','--',...
          'GridAlpha',0.15, 'Layer','top');
hold(ax, 'on');

try
    ax.XAxis.MinorTick = 'on';
    ax.YAxis.MinorTick = 'on';
    ax.TickDir = 'in';
catch
    warning('当前MATLAB版本不支持副刻度设置');
end

% 定义线型与标记组合
lineStyles = {'-'}; % 基础线型
% lineStyles = {'-', '--', '-.', ':'}; % 基础线型
markers = {'o', 's', '^', 'd', 'v', '>', '<', 'p', 'h'}; % 不同标记
markerSize = 5; % 统一标记大小

% 绘制各数据组
hLines = gobjects(nGroups, 1);
legendTexts = cell(nGroups, 1);

for i = 1:nGroups
    idx = (i-1)*2 + 1;
    plot_data = varargin{idx};
    x = plot_data(:,1);
    y = plot_data(:,2);
    % x = varargin{idx};
    % y = varargin{idx+1};
    name = varargin{idx+1};
    
    % 循环索引（超过数组长度自动循环）
    lineStyle = lineStyles{mod(i-1, numel(lineStyles)) + 1};
    marker = markers{mod(i-1, numel(markers)) + 1};
    lineColor = colors(mod(i-1, size(colors,1)) + 1, :);
    
    % 显式设置对数坐标
    % if contains(plotType, {'sx','sy','ll'})
    %     set(ax, 'XScale','log', 'YScale','log');
    % end
    
    % 统一绘图参数
    plotArgs = {'LineWidth', 1.5,...
                'Color', lineColor,...
                'LineStyle', lineStyle,...
                'Marker', marker,...
                'MarkerSize', markerSize,...
                'MarkerEdgeColor', lineColor,...
                'MarkerFaceColor', 'w'}; % 标记填充白色
    
    switch plotType
        case 'p'
            h = plot(ax, x, y, plotArgs{:});
            set(ax, 'XScale','linear', 'YScale','linear');
        case 'sx'
            h = semilogx(ax, x, y, plotArgs{:});
            set(ax, 'XScale','log',    'YScale','linear');
        case 'sy'
            h = semilogy(ax, x, y, plotArgs{:});
            set(ax, 'XScale','linear', 'YScale','log');
        case 'll'
            h = loglog(ax, x, y, plotArgs{:});
            set(ax, 'XScale','log',    'YScale','log');
        otherwise
            error('无效的绘图类型');
    end
    
    hLines(i) = h;
    legendTexts{i} = name;
end

% 坐标轴范围调整
ax.XLim(1) = ax.XLim(1)*0.85;
ax.YLim(1) = ax.YLim(1)*0.85;
ax.XLim(2) = ax.XLim(2)*1.15;
ax.YLim(2) = ax.YLim(2)*1.15;

% Latex支持设置
set(ax, 'TickLabelInterpreter','latex');
title(ax, plot_title, 'Interpreter','latex', 'FontSize',15);
xlabel(ax, plot_xlabel, 'Interpreter','latex', 'FontSize',12);
ylabel(ax, plot_ylabel, 'Interpreter','latex', 'FontSize',12);

% 图例设置
numColumns = max(ceil(nGroups/5), 1);
lgd = legend(ax, hLines, legendTexts,...
            'Location', 'best',...
            'FontSize', 13,...
            'EdgeColor',[0 0 0],...
            'Box','on',...
            'Interpreter','latex',...
            'NumColumns', numColumns);

% 打印设置
set(fig, 'PaperUnits','centimeters',...
        'PaperPosition',[0 0 18 12],...
        'PaperSize',[18 12]);
end

% For pdf
% print('-dpdf', 'output.pdf');