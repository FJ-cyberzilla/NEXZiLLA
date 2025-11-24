#!/usr/bin/env python3
import asyncio
import click
from cyber_intel_sdk import AsyncCyberIntelSDK
from cyber_intel_sdk.models.threat import ThreatIntel

@click.group()
@click.option('--base-url', default='http://localhost:8007', help='Cyber intelligence platform URL')
@click.option('--api-key', help='API key for authentication')
@click.pass_context
def cli(ctx, base_url, api_key):
    """Cyber Intelligence Platform CLI"""
    ctx.ensure_object(dict)
    ctx.obj['base_url'] = base_url
    ctx.obj['api_key'] = api_key

@cli.command()
@click.argument('target')
@click.option('--analysis-type', default='comprehensive', help='Type of analysis to perform')
@click.pass_context
def analyze(ctx, target, analysis_type):
    """Perform threat intelligence analysis"""
    async def run_analysis():
        async with AsyncCyberIntelSDK(ctx.obj['base_url'], ctx.obj['api_key']) as sdk:
            result = await sdk.analyze_threat(target, analysis_type)
            display_threat_intel(result)
    
    asyncio.run(run_analysis())

@cli.command()
@click.argument('target')
@click.option('--date', help='Forecast date (YYYY-MM-DD)')
@click.pass_context
def forecast(ctx, target, date):
    """Get threat forecast for target"""
    async def run_forecast():
        async with AsyncCyberIntelSDK(ctx.obj['base_url'], ctx.obj['api_key']) as sdk:
            result = await sdk.forecast_threats(target, date)
            display_forecast(result)
    
    asyncio.run(run_forecast())

@cli.command()
@click.argument('target')
@click.pass_context
def scan(ctx, target):
    """Perform network security scan"""
    async def run_scan():
        async with AsyncCyberIntelSDK(ctx.obj['base_url'], ctx.obj['api_key']) as sdk:
            result = await sdk.scan_network(target)
            click.echo(f"Scan results for {target}:")
            click.echo(result)
    
    asyncio.run(run_scan())

@cli.command()
@click.pass_context
def status(ctx):
    """Check system status"""
    async def check_status():
        async with AsyncCyberIntelSDK(ctx.obj['base_url'], ctx.obj['api_key']) as sdk:
            status = await sdk.get_system_status()
            click.echo("System Status:")
            click.echo(f"  Overall: {status.get('status', 'unknown')}")
            click.echo(f"  Agents: {len(status.get('agents', {}))} available")
    
    asyncio.run(check_status())

def display_threat_intel(threat_intel: ThreatIntel):
    """Display threat intelligence results"""
    click.echo(f"\n🎯 Threat Analysis for: {threat_intel.target}")
    click.echo(f"⚠️  Threat Level: {threat_intel.threat_level.value.upper()}")
    click.echo(f"🎯 Confidence: {threat_intel.confidence:.0%}")
    click.echo(f"📊 Indicators Found: {len(threat_intel.indicators)}")
    
    if threat_intel.indicators:
        click.echo("\n🔍 High-Confidence IOCs:")
        for ioc in threat_intel.get_high_confidence_iocs():
            click.echo(f"  • {ioc.value} ({ioc.type.value}) - {ioc.confidence:.0%} confidence")

def display_forecast(forecast):
    """Display threat forecast results"""
    click.echo(f"\n🔮 Threat Forecast for: {forecast.target}")
    click.echo(f"📅 Forecast Date: {forecast.forecast_date}")
    click.echo(f"📈 Predicted Risk: {forecast.predicted_risk:.0%}")
    click.echo(f"🎯 Confidence: {forecast.confidence:.0%}")
    
    if forecast.confirmed_threats:
        click.echo(f"\n✅ Confirmed Threats:")
        for threat in forecast.confirmed_threats:
            click.echo(f"  • {threat}")

if __name__ == '__main__':
    cli()
